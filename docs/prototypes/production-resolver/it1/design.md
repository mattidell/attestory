# D3 Iteration 1 — Production Package Resolver

Date: 2026-07-16  
Builder: incumbent, High tier  
Evidence ceiling: Rung 2

## Decision claims

### D3-P1 — production resolution contract

Settle at Rung 2 on a **single source-neutral resolution pipeline** with a
live-workspace source adapter. The production path does not fork the fixture
semantics. It invokes the same published-schema loader, package-integrity
checks, and typed closed-graph validator, then adds live-only guarantees:

1. the package is reached from a current adoption act at a fixed workspace
   revision, never from a caller path or directory walk;
2. the adoption act pins an immutable installed-content catalog and the exact
   package checksum;
3. every package and member read is checksum-verified after the read;
4. every contained validation issue makes the whole package set unavailable
   for execution or rendering; and
5. only the successful resolved graph can enter the production `RunContext`
   marshaller or renderer.

This is a strict guarantee superset of the fixture path: all fixture checks run
unchanged; production additionally requires current workspace adoption,
catalog anchoring, capability confinement, all-or-nothing validity, and an
exclusive graph at the live entrypoint.

### D3-P2 — discharge/defer ledger

Settle at Rung 2 on the ledger below. No ADR-0027/0028 condition is silently
treated as complete. Contract settlement here is not an implementation claim;
the rows marked “discharged by D3” become discharged in production only when
Track 3 installs the contract and its kill tests.

## Baseline findings from committed machinery

- `verify_published_package` compares the package’s recorded checksum, its
  canonical checksum, and the publication-registry checksum. It rejects a
  missing publication, self-mismatch, or version rewrite.
- `validate_package` validates each resolved citizen against its declared
  published schema and optionally compares each canonical citizen checksum to
  the citizen publication registry.
- `PackageValidation.resolved_members` is already an exclusive projection:
  only exact `package.members` pins can enter it. Corpus co-location alone does
  not confer membership.
- The synthetic fixture adapter scans directories to assemble a supply corpus
  and deliberately continues when `validation.ok` is false. That is acceptable
  fixture migration behavior but is **not** a production resolver contract.
- The committed validator accumulates member issues. “Contained” therefore
  means all defects are recorded without crashing; it does not authorize a
  partial production graph.

## Paper contract diff

### 1. Versioned adoption anchor

Add a production carrier schema, named here `act-package-adoption.v1`, before
using it. Its payload is:

```text
package: {id, version, checksum}
catalog: {id, version, checksum}
scope: {workspace_id, purpose}
```

`checksum` uses the committed canonical-JSON checksum definition. The act does
not repeat `members`; `artifact-package.v2` remains the sole membership
authority. Superseding package adoption is ordinary act supersession. At the
run’s fixed revision the resolver accepts only current, in-scope adoption acts.
The run’s `adoption` pin names this act, not a package-shaped caller assertion.

### 2. Installed-content catalog

Add `installed-content-catalog.v1` as a versioned workspace citizen:

```text
schema, id, version
objects: [{schema, id, version, checksum}]
```

The catalog is location/integrity metadata, not a manifest. It may contain
objects not named by any adopted package. Those objects remain inert. Exact
`(id, version)` keys are unique; conflicting duplicates reject. Physical
storage uses checksum-addressed objects below the live capability root, but
paths and directory contents carry no authority. The catalog checksum captured
by the adoption act prevents changing object/checksum bindings under the same
adoption.

The package entry’s catalog checksum, the adoption’s package checksum, and the
package’s `package_checksum` must all agree with the package’s recomputed
canonical checksum. A member’s catalog checksum must equal its recomputed
canonical citizen checksum. Schema publication bytes continue to be governed
by ADR-0003’s schema registry; the package does not embed schema-byte digests.

### 3. Capability-only source

```text
LivePackageSource(L_capability)
  read_current_adoption(adoption_act_id, workspace_revision)
  read_catalog(exact_catalog_pin)
  read_object(exact_id, exact_version, expected_checksum)
```

`L_capability` is runtime-only ADR-0031 capability state. No constructor accepts
a raw package path, repository-relative path, environment fallback, ignored
locator file, or directory glob. Object reads are confined beneath `L`; a
symlink, hard-link, mount, or resolved target crossing the capability root
rejects. The repository is read-only, the resolver has no publication/network
capability, and it creates no repository cache, report, patch, or locator.

Resolution is a phase of the live run. The run record starts inside `L` before
the first authoritative read. Success or failure closes that record inside
`L`; issue detail, identifiers, and dispositions never cross. This consumes
ADR-0031 Decisions 1, 4, and 7 without claiming to re-prove their installed
wall.

### 4. One resolver core

Paper signature:

```text
resolve_adopted_packages(
  source: PackageSource,
  adoption_act_ids: exact set,
  workspace_revision: int,
  schemas: DerivationSchemas,
  adopted_bundle_view: current projected act-bundle-adoption.v2 bodies,
) -> ResolvedPackageGraph | ResolutionRejected
```

For each adoption, in deterministic exact-pin order:

1. Project and validate the current adoption act at `workspace_revision`.
2. Read and checksum-verify its catalog against the adoption pin.
3. Locate the exact package entry by `(id, version)`; do not search by path.
4. Strictly parse and schema-validate the package, rejecting duplicate JSON
   keys or undeclared shapes rather than repairing them.
5. Run `verify_published_package` using the adoption-anchored catalog view.
6. Iterate `package.members`, not catalog objects or directory entries. Require
   unique exact pins. For each pin, fetch one exact catalog object, verify its
   checksum after reading, strictly validate its declared schema, and require
   its `schema`, `id`, and `version` to equal the pin.
7. Build the validation corpus **only** from those verified members. Invoke the
   committed `validate_package` with the catalog-derived checksum map.
8. Apply ADR-0028’s package-to-current-bundle nested-set equality at run bind;
   an absent, generation-swapped, omitted, or extra nested fact identity is an
   issue.
9. Accumulate all per-package issues, including quantity/composition,
   reachability, citation, producer, role-canon, and admitted-schema issues.
10. Across packages, require identical checksums for shared exact pins and
    unique output ownership unless declared conflict semantics selects an
    adopted member producer.
11. If **any** issue exists, return only `ResolutionRejected(issues)` and close
    the run record `validation-failed`. No graph or typed execution view exists.
12. Otherwise return an immutable graph containing the verified package
    instances, exact member pins, verified citizens, typed edges, output owners,
    and citation resolutions. It contains no catalog-only object and no path.

The production `RunContext` marshaller required by ADR-0032 accepts this graph
plus projected current findings. It has no overload taking rules, members,
corpus dictionaries, fixture scenarios, or filesystem paths. Rendering likewise
accepts the graph. Entrypoint reachability tests must prove that hand-assembled
`RunContext`, directory scans, and `validation.ok == false` projections cannot
reach a live run.

## Required cases and Rung-2 evidence

All probes copied the committed synthetic 2025 content into an OS-created
temporary workspace whose resolved root was outside the repository. The
temporary tree was removed automatically. No live or personal input was used.

### Case 1 — clean production resolution and fixture parity

- **Claim:** changing the byte source does not change the resolved graph.
- **Diff:** replace fixture path assembly with `LivePackageSource`; retain the
  same integrity and validation core, with the stricter success gate.
- **Behavior:** the clean `interest-slice` package accepted from both sources;
  both exclusive projections contained the same 19 exact member ids.
- **Observed graph/run:** projection equality was true, and execution over the
  scratch projection published the synthetic B1 subtotal.

### Case 2 — exclusive projection beyond fixtures

- **Claim:** co-location never grants execution or rendering authority.
- **Diff:** enumerate `package.members`; never enumerate catalog/directory
  contents into the result.
- **Behavior:** an extra valid package was present and readable in the scratch
  corpus but absent from `resolved_members`.
- **Observed graph:** `co_located_present=true`, `co_located_in_corpus=true`,
  `co_located_in_projection=false`.

### Case 3 — fail-closed byte verification (mandatory)

- **Claim:** member or package divergence prevents graph construction.
- **Diff:** verify after every source read, then make `validation.ok` mandatory.
- **Behavior:** mutating one pinned rule produced
  `MEMBER_CHECKSUM_MISMATCH`; mutating the package produced
  `PACKAGE_CHECKSUM_MISMATCH`; recomputing only its self-checksum then produced
  `PACKAGE_VERSION_REWRITE` against the anchored catalog.
- **Observed result:** all were rejects. The current validator can expose a
  reduced `resolved_members` tuple while reporting issues; the paper production
  gate deliberately makes that tuple unreachable.

### Case 4 — ADR-0031 interlock

- **Claim:** resolution is read-only with respect to repository/publication
  surfaces and all sensitive records remain in `L`.
- **Diff:** capability-only source; no raw-path constructor; in-memory graph;
  run record written only in `L`.
- **Behavior:** the probe asserted the scratch root was outside the resolved
  repository root and produced no repository artifact from scratch content.
- **Observed boundary:** Rung 2 demonstrates source separation only. The
  topology audit, guarded transport, and capability kill tests remain ADR-0031
  implementation evidence, not a D3 overclaim.

### Case 5 — no silent partial load

- **Claim:** one absent ratified member invalidates the whole adopted package.
- **Diff:** `validation.ok` is a constructor precondition for the graph.
- **Behavior:** removing the pinned line-2b citation produced `MEMBER_ABSENT`
  and `CITATION_ABSENT`; only 18 members were mechanically resolvable.
- **Observed result:** production returns `ResolutionRejected`; the 18-member
  intermediate is issue evidence, never an execution projection.

### Case 6 — discharge/defer ledger (mandatory)

| ADR item | D3 disposition | Reason / production evidence owed |
|---|---|---|
| 0027 D1, sole package authority | Discharged by D3 | Resolver selection begins only from `package.members`; extra catalog/files are inert. Track 3 co-location kill test. |
| 0027 D2, closed role canon | Discharged by D3 | Same schema/validator and role-canon checks are mandatory before graph construction. Track 3 divergence negative. |
| 0027 D3, `admitted_schemas` | Discharged by D3 | Every verified member still passes admitted-generation validation; unknown generation rejects. |
| 0027 D3, schema-byte immutability | Already discharged by ADR-0003 registry; not reopened | Package-embedded schema checksums remain **rejected**, not silently deferred. D3 uses published schema registry unchanged. |
| 0027 D4, typed outbound/inbound closure | Discharged by D3 | Full `validate_package` result gates graph construction. Track 3 missing-edge/reachability negatives. |
| 0027 D4, contained issues | Discharged by D3 | All issues are accumulated and recorded; containment never means partial execution. |
| 0027 D5, form-field producer integrity | Discharged by D3 | Existing producer/conflict checks plus cross-package owner check gate the graph. |
| 0027 D6 / PC3, package-instance immutability | Discharged by D3 | Adoption-anchored catalog + self-check + published checksum; mismatch/rewrite probed. |
| 0027 D6 / PC3, member-byte verification | Discharged by D3 | Verify every member after read against anchored catalog; mismatch probed. |
| 0027 D7 / PC1, exclusive execution projection | Discharged by D3 | Only successful graph reaches marshaller/renderer; co-located object exclusion probed. |
| 0027 PC2, selected producer for conflict | Discharged by D3 | Per-package and cross-package selection must name a verified adopted member. |
| 0027 PC4 / 0028 PC3, issue strings | Deferred as implementation detail by the ADRs | Behavior/classification is normative; exact codes may change. |
| 0027 N1 → 0028 D1–D4, exact fact surface and adoption equality | Discharged by D3, not re-deferred | Resolver consumes current `act-bundle-adoption.v2` bodies and enforces nested-set equality at run bind. Track 3 swap/omit/extra negatives. |
| 0027 N2 → 0028 D5–D8, composition obligation and quantity trigger | Discharged by D3, not re-deferred | Existing quantity, force-declare, composition-pin/member, and slot-bijection issues gate graph construction. Track 3 ADR-0028 PC1/PC1b suite. |
| 0028 D9, successor schema authority | Discharged by D3 | Declared successor schemas remain mandatory and are checked through `admitted_schemas`. |
| 0028 PC1 / PC1b, reject and non-trigger goldens | Deferred to Track 3 execution evidence | Contract behavior is fixed; full installed production negatives/non-trigger positives exceed Rung 2. |
| 0028 PC1c, confirmation round | Already complete evidence | It is historical decision evidence, not a production resolver condition. |
| 0028 PC2, migration of historical v1 bundles | Deferred to a migration milestone | Live production resolution requires residual-closed v2 content; D3 does not invent v1 exact pins. |

## Stop finding

No unrepresentable contract change was encountered. The two new carrier shapes
are explicit versioned paper diffs and therefore satisfy Article 10 at design
level; they must be published before any production instance. No production
resolver, schema, loader, validator, runner, test, or fixture was changed.
