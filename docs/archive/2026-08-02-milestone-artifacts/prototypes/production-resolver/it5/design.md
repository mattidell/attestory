# D3 Iteration 3 — Production Package Resolver (Incumbent Design)

Date: 2026-07-16  
Seat: incumbent builder, High tier  
Evidence ceiling: **Rung 2** (paper contract + throwaway synthetic scratch-`L` probes)

## Scope, ceiling, boundary, stop

**Scope.** Close only the four Iteration-2 committee blockers: (1) verified
release/registry authority, (2) current-user adoption selection, (3)
order-independent same-key candidate refusal, (4) exhaustive D3-P2 ledger
dispositions. Preserve pin-directed exclusive projection, package/member
byte verification, and `validation.ok == True` before graph, execution, or
rendering.

**Rung-2 ceiling.** Paper contract plus probes against the committed
loader/validator and a synthetic out-of-repo scratch `L`. No production
resolver, schema, fixture, or runner change is authorized or claimed installed.

**Synthetic / out-of-repo boundary.** All identifiers, packages, acts, and
registry bytes in evidence are synthetic. Live supply is scratch-`L` only
(ADR-0031 residency). No real content, locator, or personal workspace path
enters the topic.

**Stop.** Deliver only this file and `examination-it5.md`. Do not implement,
commit, review the rival, or exceed Rung 2. Stop and report if a new D1/D2
boundary, implementation claim, or weaker validation rule is required.

## 1. Verified publication release authority

### 1.1 Noun

Introduce a versioned publication citizen **`publication-release.v1`** as the
sole production **registry authority object**. It names:

- `id`, `version` — release identity
- `registry_kind` — e.g. package+citizen publication registry
- `registry_checksum` — sha256 of the **exact registry document bytes** that
  will authenticate package and member entries
- optional `issued_at` / `notes` (non-authoritative)

The release is not an `L` catalog and not a caller-selected path.

### 1.2 Pin and verify-before-use rule

The current user adoption act ( §2 ) pins:

```text
release: {id, version, checksum}
```

where `checksum` is the digest of the release citizen **or**, equivalently for
the single-registry first surface, the digest of the registry document bytes
bound by that release. Production resolution **must**:

1. Resolve registry bytes from the **immutable publication surface** keyed by
   the release identity (repo-resident published registry path determined by
   release id/version — never a working-tree path chosen by the caller, never
   an `L`-resident catalog).
2. Compute `sha256(registry_bytes)`.
3. Compare to the adoption's `release.checksum`. On inequality → typed
   `RELEASE_CHECKSUM_MISMATCH` and **halt before any entry is trusted**.
4. Only after equality, parse entries and use them to authenticate package and
   member instance digests (existing `verify_published_package` /
   citizen-checksum comparison semantics).

A substituted registry whose entries agree with forged supply still fails step 3
when the adoption pin names the true release digest. A forged `L` catalog is
never consulted for authentication.

### 1.3 What this closes

Committee A1: "immutable" without byte verification is not authority. This
contract requires **release-byte equality** before registry entries may
authenticate package/member bytes (ADR-0027 Decision 6 / PC3 direction).

## 2. Current-user adoption selection

### 2.1 Declared versioned act

Production entrypoint authority is only a declared act
**`act-package-adoption.v1`** recorded in `L` (Article 4). Required fields:

| Field | Constraint |
| --- | --- |
| `schema` | `act-package-adoption.v1` |
| `id` | stable act identity |
| `revision` | versioned act revision token |
| `actor` | **must be the user** (Ontology sole current actor) |
| `scope` | exact run scope (e.g. workspace + purpose/year) |
| `package` | exact `{id, version, checksum}` |
| `release` | exact `{id, version, checksum}` ( §1 ) |
| `supersedes` | optional prior act `id` in the same scope |
| `provenance` | non-authoritative placement note |

Caller-shaped `{package_id, version}`, fixture `adoption_pin` dictionaries, and
automation/system actors are **not** authority.

### 2.2 Selection rule (deterministic, non-caller)

At the run's fixed workspace revision and declared run `scope S`:

1. Collect all `L` records whose `schema == act-package-adoption.v1`.
2. Drop any with `actor != user`.
3. Drop any whose `scope != S`.
4. Drop any missing exact `package` or `release` pins.
5. Among remaining, compute the supersession tip set: acts whose `id` is not
   named by another remaining act's `supersedes`.
6. If the tip set is empty → `ADOPTION_NONE_CURRENT`. If size > 1 →
   `ADOPTION_AMBIGUOUS`. If size == 1 → that act is **the** current adoption.

No runner argument may select among competing acts. Stale tips remain history;
only the selected tip authorizes resolution. Non-user acts never enter the tip
set.

## 3. Pin-directed exclusive graph + same-key refusal

### 3.1 Pipeline (strict order)

1. Select current user adoption ( §2 ).
2. Verify release/registry bytes ( §1 ); load package+citizen entry maps.
3. Locate package instance bytes in `L` by exact `(id, version)` from the
   adoption package pin; refuse if absent.
4. Require `package_instance_checksum(package) == adoption.package.checksum`
   and pass `verify_published_package` against the **verified** registry
   (covers self-checksum rewrite → `PACKAGE_VERSION_REWRITE`).
5. For each `package.members` pin `K=(id,version)` in declared pin order
   (order is enumeration only; admission is digest-set based):
   - Collect **all** `L` candidates claiming key `K` (filenames irrelevant).
   - Let `D` = set of distinct `citizen_checksum` digests among candidates.
   - If `|D| > 1` → `SAME_KEY_CANDIDATE_REFUSAL` (order-independent; never
     pick the matching digest by scan order when an impostor coexists).
   - If `|D| == 0` → `MEMBER_BYTES_UNAVAILABLE`.
   - If `|D| == 1` and the sole digest ≠ registry expected →
     `MEMBER_CHECKSUM_MISMATCH`.
   - If `|D| == 1` and equals expected → admit that byte sequence.
6. Build corpus **only** from admitted pins. Co-located unpinned files are never
   candidates for unpinned keys and never enter the graph (ADR-0027 D1/D7).
7. Run committed `validate_package`. If `validation.ok != True` → refuse with
   the full issue ledger; **no** graph, execution, or rendering. Leniency and
   issue allowlists are forbidden.
8. Hand only the exclusive resolved member graph to the production marshaller
   (ADR-0032 consumption; not claimed installed here).

### 3.2 Guarantee posture

This production path is a **strict superset** of fixture guarantees: every
fixture integrity/validation check remains; production adds verified release
authority, current-user adoption, same-key refusal, and the hard `ok == True`
gate the fixture CLI deliberately omits.

## 4. D3-P2 exhaustive disposition matrix

Allowed dispositions only: **contract settled here** | **production condition
(owning track)** | **deferred (reason)** | **N/A**.

"Contract settled here" means the paper production resolver **defines** how the
condition is enforced at the `L` boundary. It is **not** an installed Track-3
discharge. Installed D1/D2 work is never a D3 discharge.

### 4.1 ADR-0027

| Item | Disposition | Note |
| --- | --- | --- |
| D1 sole package authority | contract settled here | Only `package.members` pins admit; no walk/catalog authority |
| D2 role canon | contract settled here | Closed role vocabulary via validation before graph |
| D3 admitted schemas / embedded schema-byte checksums | N/A | Embedded schema-byte checksums **rejected** (not deferred); generation admission remains via `admitted_schemas` + ADR-0003 registry |
| D4 typed closure / contained issues | contract settled here | Contained issues recorded; production requires `ok == True` before graph |
| D5 form-field producer integrity | contract settled here | Enforced inside validation gate (conflict without selectable producer → issue → refuse) |
| D6 package-instance immutability | contract settled here | Release-verified registry + package pin + `verify_published_package` |
| D7 exclusive execution projection | contract settled here | Pin-directed graph; unpinned inert |
| PC1 co-located unpinned golden | production condition (Track 3/4) | Behavior settled; installed golden suite owed by tracks |
| PC2 conflict_semantics golden | production condition (Track 3/4) | Behavior settled; golden owed by tracks |
| PC3 registry-verified package/members | contract settled here | Release-byte verify then entry verify; Track 3 installs |
| PC4 issue code strings | N/A | Implementation detail; classifications normative |

### 4.2 ADR-0028

| Item | Disposition | Note |
| --- | --- | --- |
| D1 versioned fact-type/bundle members | contract settled here | Enforced by validation under `ok == True` gate |
| D2 dual pin unit / F(P) | contract settled here | Same |
| D3 wholesale nested-set equality | contract settled here | Act-bundle adoption equality at bind remains ADR-0028; package resolution refuses if validation fails |
| D4 exact mapping fact-type edges | contract settled here | Mapping pins must lie in F(P) or issues fire |
| D5 composition obligation authority | contract settled here | Package-declared obligations checked in validation |
| D6 full composition binding per S | contract settled here | Missing pin/member → issues → refuse |
| D7 mandatory closed quantity vocabulary | contract settled here | Missing/unknown quantity → issues → refuse |
| D8 force-declare same-quantity | contract settled here | Structural force-declare in validation |
| D9 schema successors / admitted_schemas | contract settled here | Residual schema gens must be admitted |
| PC1 reject-direction goldens | production condition (Track 4) | Contract exists; goldens are track work |
| PC1b accept/non-trigger goldens | production condition (Track 4) | Same |
| PC1c confirmation readiness | N/A | Confirmation already complete for ADR-0028 ratification |
| PC2 historical v1 migration | deferred | Implementation migration of v1 bundles; residual pins target versioned citizens only |
| PC3 issue-code strings | N/A | Implementation detail |

### 4.3 Consumed interlocks (not D3 discharges)

| Item | Disposition | Note |
| --- | --- | --- |
| ADR-0031 D1 residency wall | production condition (Tracks 1/3) | D3 reads `L` under the wall; does not install or claim the wall |
| ADR-0032 marshal-only live entrypoint | production condition (Tracks 2/3) | Graph feeds marshaller only after success; kill-test proof not claimed |

## 5. RG-1 — MUST production prerequisite

The committed synthetic core package
`tax.us.2025.package.core-calculations@v1` validates with **`ok == False` and
exactly eight issues** under the committed validator (observed codes:
`SCHEMA_NOT_ADMITTED`, `ROLE_MISMATCH`, two `MAPPING_FACT_TYPE_NOT_ADMITTED`,
four `MEMBER_UNREACHABLE`).

**RG-1 (MUST before any live production run):**

1. **Validator-reachability repair** — eliminate the four `MEMBER_UNREACHABLE`
   defects (entrypoint/root reachability for vocabulary and default parameters).
2. **v1-generation content debt** — eliminate `SCHEMA_NOT_ADMITTED` /
   `ROLE_MISMATCH` on residual v1 rule content and the two mapping fact-surface
   admissions so the package's fact surface closes under ADR-0028.

No leniency, partial graph, or issue allowlist may substitute for RG-1. The
strict `validation.ok == True` gate remains mandatory.

## 6. Non-claims

- No production code, schema file, or fixture is installed by this iteration.
- D1 wall topology/capability proof and D2 marshal-only kill-test remain track
  work.
- Issue string spelling remains non-normative (PC4 / 0028 PC3).
- Embedded schema-byte checksums remain **rejected**, never deferred to a future
  "maybe install."
