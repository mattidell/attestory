<!-- foreman-context-v1
{
  "version": 1,
  "topic": "k1-interest-breadth",
  "milestone_state": "closed",
  "status": "CLOSED. The bounded Form-1065 K-1 box-5 taxable-interest path is synthetic complete through line 2b, composition-complete Schedule B Part I, downstream results, package resolution, explanation, and presentation. Independent review returned READY, and the closing-CI stale v2 test expectation was repaired.",
  "scope": [
    "add an authoritative, horizon-closed source family for 2025 Schedule K-1 (Form 1065) box-5 taxable interest",
    "publish a successor positive-interest composition and Form 1040 line-2b producer that include the K-1 family without relabeling it as non-form interest",
    "replace Schedule B's temporary box-1-only Part-I simplification with a versioned generic multi-family itemization contract whose row sets are structurally complete against the declared composition",
    "carry the new path through contribution, lifecycle, package and release resolution, downstream recomputation, explanation, and presentation on production-shaped synthetic fixtures",
    "preserve every historical schema, content citizen, package, registry, release, adoption fixture, and accepted ADR byte-for-byte"
  ],
  "non_goals": [
    "no Schedule K-1 from Form 1120-S or Form 1041, no Schedule K-3, and no Schedule K-1 box other than Form 1065 box 5",
    "no partnership basis worksheet, passive-activity calculation, publicly traded partnership handling, investment-interest deduction, clean-renewable-energy-bond basis adjustment, or other partnership tax computation",
    "no market discount, nominee interest, accrued-interest-at-purchase adjustment, bond-premium amortization, seller-financed mortgage, or other positive or subtractive interest source",
    "no Schedule D, Form 8949, Form 1099-B, transaction-level gain or loss, or claim of general capital-gains support",
    "no edit, reformat, move, deletion, or checksum rewrite of a published schema or historical versioned citizen",
    "no real-data run, owner attestation, entry-surface work, filing, transmission, security hardening, historical migration, or unrelated UI redesign",
    "no personal values, identifiers, dispositions, workspace locations, documents, screenshots, or generated private artifacts"
  ],
  "retrospective": "docs/milestone-retrospectives/2026-07-31-k1-interest-breadth.md",
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-31-k1-interest-breadth-builder.md",
      "docs/phases/engine-breadth/milestones/k1-interest-breadth.md",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0026-taxable-interest-composition-and-line-2b.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/content/tax/2025/interest-composition.json",
      "packages/content/tax/2025/rule.form1040-line2b.json",
      "packages/content/tax/2025/rule.attachment.schedule-b.json",
      "packages/content/tax/2025/form1040.line-2b.form-field.v2.json",
      "packages/content/tax/2025/package.core-calculations.v8.json",
      "packages/derivation/package_validation.py",
      "packages/derivation/runner.py",
      "packages/derivation/marshal.py",
      "packages/derivation/live.py",
      "packages/derivation/presentation_projection.py",
      "tests/tax/test_track2_line2b.py",
      "tests/test_dsbs_t2_schedule_b.py",
      "tests/test_frrs_t3_resolver_bootstrap.py",
      "tests/test_presentation_l2_integration.py",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-31-k1-interest-breadth-builder.md",
      "docs/phases/engine-breadth/milestones/k1-interest-breadth.md",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0026-taxable-interest-composition-and-line-2b.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/derivation/package_validation.py",
      "packages/derivation/runner.py",
      "packages/derivation/marshal.py",
      "packages/derivation/live.py",
      "packages/derivation/presentation_projection.py",
      "tests/tax/test_track2_line2b.py",
      "tests/test_dsbs_t2_schedule_b.py",
      "tests/test_frrs_t3_resolver_bootstrap.py",
      "tests/test_presentation_l2_integration.py",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol",
      "PROJECT_PLANNING.md#Milestone Closeout"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-07-31-k1-interest-breadth.md",
      "docs/phases/engine-breadth/engine-breadth-overview.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md",
      "docs/phases/engine-breadth/milestones/k1-interest-breadth-deferral-ledger.md",
      "docs/phases/engine-breadth/milestones/k1-interest-breadth.md"
    ]
  }
}
-->
# Milestone: Schedule K-1 Box-5 Interest Breadth

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by the owner 2026-07-31.

## Objective

Make one additional valid-return class computable end to end: an individual
2025 federal return containing taxable interest reported in box 5 of Schedule
K-1 (Form 1065).

The new amount enters its own horizon-closed source family, participates
explicitly in Form 1040 line 2b, appears in Schedule B Part I whenever Schedule
B is required, propagates through the existing downstream return, and reaches
the explanation and presentation surfaces through a verified package release.

## Current state

ADR-0026 defines line 2b as a closed composition of four positive source
families: Form 1099-INT boxes 1 and 3, taxable OID, and explicitly enumerated
non-form interest. It names Schedule K-1 interest as deferred work and forbids
the residual non-form label from silently absorbing it.

The production package is `tax.us.2025.package.core-calculations@v8`, resolved
through `published-packages.v3` and `demo.release.2025@v3`. Its line-2b rule,
composition, Schedule B rule, and selected line-2b field are all historical v1
citizens. A newer `form-field.v3` line-2b content version v2 is published but
is not selected by the v8 graph. The v9 graph must select the new line-2b field
content version v3 directly; it does not route through v2.

Schedule B's requirement conditional already reads the full taxable-interest
total, so K-1 interest would affect whether the attachment is required as soon
as line 2b includes it. Its Part-I content, however, intentionally collects and
ties out only the Form 1099-INT box-1 family. That simplification must be
retired in the same milestone; otherwise a K-1 amount could require Schedule B
while remaining absent from the schedule's interest rows.

## Official 2025 tax boundary

The following official instructions ground the selected tax routing:

- [Partner's Instructions for Schedule K-1 (Form 1065), box 5](https://www.irs.gov/instructions/i1065sk1)
  direct an individual partner to report box-5 interest on Form 1040 or
  1040-SR, line 2b.
- [Instructions for Form 1065, line 5](https://www.irs.gov/instructions/i1065)
  define the source as taxable portfolio interest and direct the partnership
  to report each partner's share in Schedule K-1 box 5.
- [Instructions for Schedule B (Form 1040), Part I](https://www.irs.gov/instructions/i1040sb)
  require line 1 to report all taxable interest and retain the strictly-over-
  $1,500 attachment trigger already represented by the package.

This milestone supports only the Form 1065 K-1 box-5 amount that routes to line
2b. A statement concerning clean renewable energy bond credits does not change
that line-2b inclusion, but its separate partnership-basis adjustment is not
computed here.

## Streamlined milestone process

The owner directed a lighter process for this named milestone.

- **Establish scope:** applies through this planning unit and the executable
  Builder work packet.
- **Rival prototypes:** skipped. The new contracts below are monotonic
  successors to accepted source-family, interest-composition, attachment, and
  package contracts; no competing product shape is being selected.
- **Review and repair:** one independent integrated review after the complete
  Builder implementation. One bounded repair cycle is available for concrete
  findings. A second substantive defect returns to the owner.
- **Establish the scope contract:** applies in this plan's Contracts section.
  A new ADR is not planned. If implementation cannot honor these contracts
  without changing an accepted decision, the Builder stops.
- **Build:** one integrated Builder packet, one milestone branch, and one
  implementation PR/closing PR rather than separate PRs per internal track.
  Foreman closeout is bookkeeping, not a separate reviewed implementation
  track.

## Scope

As the capsule's `scope`.

## Non-goals

As the capsule's `non_goals`.

## Contracts

### K1-C1 — Source identity, value, and closure

The selected member is the taxable-interest amount in box 5 of one logical
2025 Schedule K-1 (Form 1065) furnished by one partnership to the return
subject.

- The fact identity is tax year + partnership entity + logical K-1 statement
  entity. The subject remains in act scope, following existing fact identity.
- The statement entity is peer to evidence. File, upload, scan, document, and
  evidence identifiers never enter fact identity.
- Two original K-1s from the same partnership remain distinct through distinct
  logical statement entities. A corrected copy of the same logical K-1 answers
  the same fact and supersedes its prior finding.
- The value is a nonnegative number carrying the existing taxable-interest
  quantity. A negative contribution is invalid and fails atomically.
- A dedicated source family claims exactly all Form 1065 K-1 box-5 taxable-
  interest amounts for 2025. It does not claim other K-1 forms, boxes, attached
  statements, total taxable interest, or partnership-basis completeness.
- Its closure is keyed to the current family horizon and authorizes only its
  dedicated subtotal, including an honest closed-empty zero. A late member
  advances the horizon and displaces the old closure and every consumer.

The implementation publishes a dedicated fact-type bundle, source family,
closure mapping, subtotal rule, and IRS citation citizen. The subtotal rule is
a cited `rule-artifact.v3` citizen and uses existing collect/round behavior.

### K1-C2 — Successor positive-interest composition

Publish `tax.us.2025.interest-composition@v2` under the existing
`taxable-interest-composition.v1` schema. Its five-slot bijection is exactly:

1. Form 1099-INT box 1;
2. Form 1099-INT box 3;
3. taxable Form 1099-OID box 1;
4. enumerated non-form positive interest; and
5. Schedule K-1 (Form 1065) box-5 taxable interest.

Publish `tax.us.2025.rule.form1040-line2b@v2` as a cited
`rule-artifact.v3` successor. It references, pins, sums, and `require_closed`s
all five subtotals/families. Package validation must reject every omission,
duplicate, substitution, extra slot, wrong family/subtotal pairing, absent
composition binding, and mixed v1/v2 graph.

The existing line-2b symbol remains unchanged so line 9 and downstream rules
consume the successor without unrelated version churn. Publish a line-2b
form-field content version v3 whose description and disposition explanations
name the five-family boundary. Historical field versions remain unchanged.

### K1-C3 — Multi-family attachment itemization

Publish `attachment-rule.v2` as an additive schema successor; never edit
`attachment-rule.v1`. Version 2 preserves ADR-0036's three atomic attachment
dispositions, requirement conditional, presence-before-value completeness,
categorical answer domain, obligation naming, attachment-only tie-out failure,
and per-row input pins.

Its itemization surface adds explicit authority for a whole logical part:

- a **single-family authority** names one source-family declaration;
- a **composition authority** names one adopted composition declaration;
- a part contains one or more `row_sets`; each row set uses
  `collect_members`, names its family-authorized subtotal, and retains the
  same-family/current-horizon/per-member-pin semantics;
- the part names one final `line_symbol` tie-out.

Package validation enforces:

- every row set's member fact type equals its source family's canonical member
  predicate;
- every row set's subtotal equals that family's `authorizes_subtotal`;
- a single-family part has exactly one matching row set and ties to that
  subtotal;
- a composition-backed part's row sets form an exact family/subtotal bijection
  with the pinned composition and its final line symbol equals the
  composition's `publishes` symbol; and
- no duplicated or extra row-set family can pass admission.

At runtime, each row-set sum ties to its family subtotal, then the combined
part sum ties to the declared line symbol. Either mismatch emits
`ITEMIZATION_TIE_OUT_VIOLATION`, blocks only the attachment, and publishes no
divergent attachment value.

Publish `tax.us.2025.rule.attachment.schedule-b@v2` using composition authority
for Part I over all five positive-interest families. Part II remains a
single-family itemization over ordinary dividends. Part III behavior remains
unchanged. This replaces the v1 box-1-only simplification without changing the
historical rule.

Because production packages currently admit only `attachment-rule.v1`, publish
an additive `artifact-package.v6` schema that admits v2 under the existing
`attachment-rule` member role while preserving all v5 members. Supply fully
resolved positive examples and isolated negatives for both new schemas, append
their manifest entries with the registry writer, and confirm existing manifest
entries are byte-identical.

### K1-C4 — Publication, release, explanation, and presentation

Publish one coherent successor route:

- `tax.us.2025.package.core-calculations@v9` under `artifact-package.v6`;
- `published-packages.v4` containing the new and historical citizen checksums;
- `demo.release.2025@v4`; and
- an obviously synthetic current adoption of package v9/release v4.

The v9 graph resolves exactly one current version of every successor citizen
and no mixed interest or Schedule B graph. Every input byte is checksum-
verified before execution. Existing v8/v3 and earlier package/release/adoption
fixtures remain unchanged and resolvable.

Explanation and presentation must expose the K-1 amount only through the
derived line-2b and Schedule B results, with exact citation identity and no
rejected value. `live_coordinate_run` is the authoritative integration surface;
direct `RunContext` tests are allowed only for impossible-to-construct tie-out
kill cases, as in the existing attachment tests.

### K1-C5 — Compatibility and stop boundary

The new work is additive. It must not mutate accepted ADRs, published schemas,
historical content citizens, v1/v2 line-2b fields, package v8 or earlier,
published registries v1-v3, releases v1-v3, or their adoption fixtures.

Stop rather than improvise if:

- a faithful K-1 identity requires actor, evidence, or document identity in a
  fact key;
- the multi-family part cannot preserve ADR-0036's same-family row authority,
  atomic dispositions, or attachment-only failure boundary;
- a fully resolved positive instance for either new schema cannot be written
  honestly;
- the v9 graph requires revising a historical checksum or selecting two
  current producers for one symbol;
- the official box-5 routing conflicts with the bounded Form 1065 scope; or
- implementation turns on governance interpretation or a reserved/deferred
  ontology entry.

## Readiness inventory

The Builder must reconcile this inventory against the base before editing and
report any omitted seam as a charter stop.

| Surface | Current base | Required successor or change |
| --- | --- | --- |
| Source facts | No K-1 citizens | Bundle with nonnegative box-5 amount and horizon closure fact |
| Identity | 1099 statement precedent only | Partnership + logical Form-1065 K-1 statement + tax year |
| Family authority | Four positive-interest families | K-1 family, mapping, subtotal, closure lifecycle |
| Composition | `interest-composition@v1`, four slots | `@v2`, exact five-slot bijection |
| Line 2b | rule v1, field content v2 | cited rule v2 and field content v3 |
| Schedule B | attachment rule v1, Part I box-1 only | `attachment-rule.v2` and Schedule B content v2 |
| Package schema | `artifact-package.v5` | additive v6 admitting attachment-rule.v2 |
| Package route | core v8 / registry v3 / release v3 | core v9 / registry v4 / release v4 / adoption v9 |
| Runtime | v1 attachment dispatch in runner, marshal, live, validation, projection | accept v1 unchanged and execute/validate/project v2 |
| Downstream | line 9 consumes stable line-2b symbol | recompute with K-1 value; no line-9 content successor expected |
| Explanation | legacy line-2b rule has no declared citations | cited rule v2 and exact form-field citation chain |
| Fixtures | no K-1 production-shaped workspace | synthetic positive, blocked, lifecycle, package, Schedule B, and presentation cases |

## Builder and reviewer verification package

The case IDs below are the shared acceptance vocabulary. The Builder must
implement evidence for every row or stop with a precise reason. The independent
Reviewer will assess these same cases, attack omitted neighbors, and rerun only
load-bearing claims rather than repeat routine CI.

### Positive and boundary cases

| ID | Scenario | Required observation |
| --- | --- | --- |
| K1-P1 | One $80 Form-1065 K-1 box-5 member; every interest family closed | K-1 subtotal and line 2b publish $80; downstream line 9/taxable income recompute; pins include all five subtotals and closures |
| K1-P2 | $80 K-1 plus existing $1,000 Form 1099-INT box 1 | Line 2b publishes $1,080 with distinct source-family provenance; K-1 is never classified as non-form interest |
| K1-P3 | Two original K-1 statements from the same partnership | Distinct statement identities both contribute and subtotal exactly once |
| K1-P4 | Corrected copy of one logical K-1 changes $80 to $90 | Same fact identity; prior finding and downstream publications become non-current; rerun publishes $90 |
| K1-P5 | K-1 family closed empty | K-1 subtotal publishes honest zero and existing non-K-1 return values remain unchanged |
| K1-P6 | Total taxable interest exactly $1,500 and no other Schedule-B trigger | Schedule B is inapplicable; strict-greater-than boundary is unchanged |
| K1-P7 | K-1 interest alone is $1,501 | Schedule B publishes when Part III is complete; Part I contains the K-1 row and ties to line 2b |
| K1-P8 | $1,000 Form 1099-INT box 1 plus $600 K-1 | Combined threshold triggers; both row sets tie to their family subtotals and combined Part I ties to $1,600 |
| K1-P9 | Dividends trigger Schedule B while K-1 interest is below threshold | Published Schedule B still contains every current Part-I interest row, including K-1 |
| K1-P10 | Existing v8/release-v3 adoption | Historical package resolves and existing synthetic outputs remain byte/semantics compatible |

### Honest-block, lifecycle, and rejection cases

| ID | Mutation or condition | Required observation |
| --- | --- | --- |
| K1-N1 | K-1 family unclosed, empty or nonempty | K-1 subtotal may exist but line 2b blocks on the family closure; line 9 and dependent results do not publish from an incomplete universe |
| K1-N2 | Late K-1 member after a current closure | Horizon advances; old closure and line-2b/downstream publications leave current state until successor-horizon closure and rerun |
| K1-N3 | Negative box-5 amount | Contribution/admission fails atomically; no member transition or partial fact lands |
| K1-N4 | Evidence/file identifier substituted for logical statement identity | Schema or admission rejects; no evidence identity enters the fact key |
| K1-N5 | Composition omits, duplicates, substitutes, or adds a family/subtotal | Package validation rejects the v9 graph |
| K1-N6 | Line-2b successor omits the K-1 ref, pin, `require_closed`, or composition binding | Package validation rejects; no narrow producer can win the line-2b symbol |
| K1-N7 | Multi-family Part I omits K-1 or another v2 composition slot | Package validation rejects even when the omitted family's runtime value would be zero |
| K1-N8 | A row set uses the wrong member fact type or wrong family subtotal | Package validation rejects before execution |
| K1-N9 | Duplicate or extra Part-I row-set family | Package validation rejects before execution |
| K1-N10 | Stale row set disagrees with its family subtotal | Schedule B alone blocks with `ITEMIZATION_TIE_OUT_VIOLATION`; line 2b remains published |
| K1-N11 | Family row sets each tie, but combined Part-I total disagrees with line 2b | Schedule B alone blocks with `ITEMIZATION_TIE_OUT_VIOLATION`; no divergent attachment publishes |
| K1-N12 | Package v9 mixes composition v2 with line-2b v1, Schedule-B v1, or line-2b field content v1/v2 | Resolver/package validation refuses the mixed graph |
| K1-N13 | Presentation receives a rejected/non-numeric K-1-derived value | Value is redacted and failure remains section-contained under the existing presentation contract |

### Reviewer attack checklist

The independent review must answer, with evidence:

1. Is the supported source exactly Form 1065 Schedule K-1 box 5, with every
   neighboring K-1 form/box still outside the claim?
2. Can same-partnership originals, corrections, and evidence replacement occur
   without identity collision or duplicate counting?
3. Does every line-2b publication depend on all five current family closures,
   including present nonzero families?
4. Can any package-valid v2 Part-I declaration omit a composition member,
   duplicate one, or tie a row set to the wrong subtotal?
5. Do both tie-out layers fail only the attachment and pin all rows actually
   consumed?
6. Does v9 resolve exactly one successor graph while v8 and earlier remain
   valid and unchanged?
7. Do citation walking, blocked-value redaction, and presentation projection
   work through `live_coordinate_run`, not a fixture-only shortcut?
8. Were any published schema bytes or historical checksums changed, even if
   their manifests were regenerated to match?
9. Do the fixtures use only `demo.*` / `demo-*` identities and avoid absolute
   paths, private outputs, or real values?
10. Did the implementation add any market-discount, adjustment, other K-1,
    partnership-basis, Schedule-D, filing, or UI behavior outside the charter?

## Fixtures

Commit a focused synthetic fixture family under a new K-1 breadth directory.
Use obviously synthetic partnerships, logical statement IDs, contribution IDs,
family horizons, findings, and run IDs. Include:

- one K-1-only return;
- mixed Form 1099-INT + K-1 return;
- same-partnership multiple statements;
- correction and late-member lifecycle sequences;
- exact-threshold and combined-threshold Schedule B cases;
- required-and-complete and required-and-incomplete Schedule B cases;
- package v9/release v4/adoption v9 resolution; and
- at least one production-shaped presentation model generated from
  `live_coordinate_run`.

Regenerate only new successors and the new fixture family. Existing goldens
must remain unchanged unless the plan explicitly names a compatibility fixture
whose current-package selector is intentionally advanced; inspect every such
diff rather than accepting generator output wholesale.

## Verification

The integrated Builder charter names exact commands. At minimum the evidence
must include:

- focused new source/composition/Schedule-B/package/presentation modules;
- `tests.test_schema_registry` and manifest-addition inspection;
- existing line-2b, Schedule B, resolver, presentation, and capital-gain
  compatibility modules touched by the successor route;
- repository mypy for typed Python changes;
- `git diff --check`;
- governance lint; and
- the envelope scan over the complete branch range.

CI `verify` remains the gate of record. Do not repeatedly rerun the full suite
locally.

## Data safety

No personal or real tax data is needed. All committed acts, values, identities,
workspaces, reports, and presentation artifacts are synthetic and publishable.
No local absolute path or ignored local output may enter a fixture, manifest,
review, or planning record.

## Exit criteria

The milestone is complete when:

1. K1-P1 through K1-P10 and K1-N1 through K1-N13 have committed evidence or an
   explicit, reviewer-accepted equivalence to a stronger case;
2. package v9/release v4 computes the bounded K-1 class end to end through the
   authoritative coordinator and presentation surfaces;
3. Schedule B Part I is structurally complete against interest composition v2,
   with both tie-out layers enforced;
4. every historical schema/content/package/registry/release fixture remains
   immutable and compatible;
5. an author-independent Reviewer returns `READY`, or all blocking findings
   are repaired and independently rechecked within the one-cycle cap;
6. the closing PR's `verify` check is green and the owner merges it; and
7. the coverage frontier, roadmap, phase state, deferral ledger, and concise
   retrospective accurately record the bounded result without a real-data or
   broader-K-1 claim.

## Execution record

| Unit | Result |
| --- | --- |
| Scope and contracts | The committed plan defined K1-C1–C5 and the shared K1-P1–P10 / K1-N1–N13 verification matrix. A pre-build inventory correction recorded that package v8 selected line-2b field content v1, not the separately published v2. |
| Integrated build | The Builder completed the additive source-family, composition, attachment-rule, package/release, runtime, fixture, explanation, and presentation route on `milestone/k1-interest-breadth`. |
| Independent review | `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-31-k1-interest-breadth-review.md` returned `READY` for the exact implementation range. It confirmed the full case matrix, publication history, safety envelope, package compatibility, and focused static checks. |
| Repair | Closing PR #133 exposed one stale current-version assertion in `tests/test_dsbs_t1_schema_citizens.py`. The bounded repair advanced only the method name and expected current field version from v2 to v3; product behavior and historical citizens were unchanged. |
| Closeout | The roadmap, coverage frontier, phase state, deferral ledger, and retrospective record only the bounded synthetic-complete claim. PR #133's replacement green `verify` check and owner merge are the ratification boundary. |

## Execution sequence

### Track 1 — Integrated source-to-presentation build

One Builder implements K1-C1 through K1-C5 and the complete case matrix in
dependency order: schemas/examples first; source/family/composition content;
attachment v2 machinery and content; package/release route; coordinator,
lifecycle, explanation, and presentation evidence. Keep separable commits for
schema publication, content/runtime, and integrated fixtures if that makes
review clearer, but do not create additional role or PR gates.

### Integrated independent review

After the Builder hands off a clean branch, the Foreman files an exact-range
Reviewer charter that incorporates this plan and the Builder work packet. The
Reviewer uses the attack checklist above, reruns load-bearing cases, and returns
one integrated verdict.

### Repair and closeout

Concrete findings return to the same Builder for one bounded repair cycle. The
same Reviewer rechecks only changed behavior and adjacent invariants that the
repair could affect. The Foreman then performs closeout records and opens the
single closing PR.
