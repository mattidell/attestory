# D3 Iteration-3 Clean-Room Rival — Production Package Resolver Design

Date: 2026-07-16. Seat: Iteration-3 clean-room rival, High. Evidence: Rung 2
(paper contract + throwaway synthetic scratch-`L` probes against committed
loader/validation). All identifiers, packages, acts, and paths are synthetic.
No production code, schema, loader, validator, runner, or fixture is modified.

**Seal:** sealed from incumbent (`it5/`, `examination-it5.md`, and other
incumbent designs) until foreman custody. Independent authority-chain design.

## 0. Scope and non-goals

This design answers only the four Iteration-2 committee blockers:

1. **Verified publication authority** — a versioned release whose bytes are
   verified before any registry authenticates package or citizen bytes.
2. **Current-user adoption selection** — exactly one current Article-4 user act
   selected by declared scope/revision/currency; not caller metadata.
3. **Order-independent same-key refusal** — pin-directed supply that refuses
   ambiguous same-key candidates independent of filesystem enumeration.
4. **Precise D3-P2 ledger** — one disposition per ADR-0027 D1–D7 / PC1–PC4 and
   ADR-0028 D1–D9 / PC1, PC1b, PC1c, PC2, PC3.

Non-goals: D1 wall implementation (ADR-0031 consumed), D2 marshaller proof
(ADR-0032 consumed), embedded schema-byte checksums (rejected by ADR-0027 D3),
N1/N2 re-litigation (closed by ADR-0028), tax content, OCR/UI.

---

## 1. Authority chain (D3-P1)

Resolve proceeds as a single fail-closed pipeline. Any step failure yields **no
resolved member graph**, no execution, no rendering. Partial graphs are not
returned.

```
current user adoption act
  → verify release bytes (pinned)
  → bind registry bytes (release-attested)
  → verify package instance (registry + adoption pin)
  → pin-directed member admission (registry + pins)
  → validate_package → require ok == True
  → exclusive resolved member graph
```

### 1.1 Versioned release citizen (publication root)

Introduce a synthetic publication-root citizen (Track-3 schema; paper shape now):

| Field | Rule |
| --- | --- |
| `schema` | `release-registry.v1` (declared generation) |
| `id`, `version` | immutable release identity |
| `registry_sha256` | SHA-256 of the exact registry document bytes this release attests |
| (optional) `citizen_registry_sha256` | same for a split citizen registry document |

**Release digest** = SHA-256 of the canonical release citizen bytes (sorted keys,
no self-checksum field participating).

**Verification rule (normative):** before any package or citizen authentication,
the resolver:

1. Loads the release citizen indicated by the adoption act’s release pin
   `(id, version, checksum)`.
2. Recomputes the release digest; inequality → `RELEASE_BYTE_MISMATCH` (reject).
3. Loads the registry document the release attests; recomputes its SHA-256;
   inequality with `registry_sha256` → `REGISTRY_BYTE_MISMATCH` (reject).
4. Only then materializes entry maps via the committed
   `load_published_*_checksums` shape over those **verified** bytes.

A caller-selected registry file, an `L` catalog, or a working-tree path is **not**
authority. Replacing release bytes to agree with a forged registry fails step 2
against the adoption pin. Replacing registry bytes under an honest release fails
step 3. Entry rewrite under an honest release+registry fails the existing
`verify_published_package` / citizen checksum compare (PACKAGE_VERSION_REWRITE /
citizen mismatch).

Repo-resident public registries remain the intended physical home of release and
registry documents; `L` may hold **candidate copies** only. Candidates become
usable solely when their digests equal the pinned release and attested registry
digests. Unverified candidate registries never authenticate supply.

### 1.2 Current-user package adoption act

Declare carrier `act-package-adoption.v1` (Article 4 adoption; Ontology §1 sole
current actor is the user; §4 adoption is that user’s immutable, scoped,
versioned act).

Required fields (paper):

- `act_id` — durable act identity
- `actor.kind == "user"` and `actor.id` equal to the workspace’s sole user
- `scope` — exact structured scope (e.g. workspace identity, tax year, jurisdiction)
- `revision` — non-negative integer position in the scope’s act sequence
- `package` — `{id, version, checksum}` exact package-instance pin
- `release` — `{id, version, checksum}` exact release pin (publication root)
- `supersedes` — optional prior `act_id` in the same scope
- `recorded_at` — timestamp for audit only; **not** a selection key

**Forbidden actors:** `system`, `automation`, caller process identity, CI, or any
non-user kind. Such acts are ineligible; they never become current.

**Currency selection (normative, order-independent):**

1. Consider only acts with `schema == act-package-adoption.v1`.
2. Drop acts whose `actor` is not the sole user.
3. Drop acts whose `scope` does not equal the run’s declared scope.
4. Drop acts missing well-formed exact `package` and `release` pins (64-hex
   checksums).
5. Apply supersession: if act B lists `supersedes: A`, drop A when both remain
   eligible.
6. Among remaining, select the unique act with maximum `revision`.
7. If zero eligible → `NO_CURRENT_USER_ADOPTION`. If two or more share the max
   revision → `AMBIGUOUS_CURRENT_ADOPTION`. Both refuse; no caller tie-break.

Shuffling act storage order must not change the selected `act_id`. Competing
stale user acts lose to the higher revision (or to an explicit supersession).
Non-user acts never win. The run request may name a workspace/scope locator; it
must not name a package id, release digest, or act id as authority — those come
only from the selected act.

### 1.3 Pin-directed, order-independent supply

After release+registry verification and package-instance verification against the
adoption package pin:

For each package member pin `(member_id, version)`:

1. Collect **all** candidate byte bodies under `L` (and any admitted corpus
   roots) that declare that exact `(id, version)`.
2. Compute each candidate’s `citizen_checksum` (committed canonical SHA-256).
3. Let `expected` be the registry-verified citizen checksum for that key (and,
   when the package pin table carries a member digest, that digest must equal
   `expected` — dual mismatch still rejects).
4. Keep candidates whose checksum equals `expected`.
5. Outcomes:
   - zero matches → `MISSING_PINNED_BYTES` (reject whole resolve)
   - one match → admit that body
   - multiple matches with identical checksum → collapse to one (byte-identical)
   - multiple distinct checksums cannot all equal `expected`; if the filter ever
     yields ambiguity, `AMBIGUOUS_SAME_KEY` (reject)

Filesystem enumeration order, glob order, and directory layout **must not**
affect admission. Co-located unpinned files are never opened as members: they
are not in the pin table, so they never enter the candidate filter for any pin.
A same-key evil candidate co-located with the honest bytes is ignored when its
checksum differs; it cannot race into the graph by appearing first.

Missing any pinned member → refuse; **no partial graph**.

### 1.4 Validation gate and exclusive projection

On the admitted member set only, invoke committed `validate_package` (typed
closed-graph validation). **Hard gate:**

- If `validation.ok is not True` → reject resolve; return issues; **no graph**,
  no execution, no rendering.
- If `ok is True` → the exclusive resolved member graph is exactly the admitted
  pin-directed set; nothing else is executable or renderable (ADR-0027 D7).

This is a strict **superset** of the fixture path’s integrity checks: the
fixture CLI currently continues when `ok` is false; production must not.
Committed measurement: synthetic core package
`tax.us.2025.package.core-calculations@v1` yields `ok=False` with **eight**
issues (SCHEMA_NOT_ADMITTED, ROLE_MISMATCH, two× MAPPING_FACT_TYPE_NOT_ADMITTED,
four× MEMBER_UNREACHABLE). Synthetic
`tax.us.2025.package.interest-slice@v1` yields `ok=True` with zero issues under
the same corpus/registry — the clean-success reference.

### 1.5 RG-1 (MUST production prerequisite)

**RG-1** is not discharged by this paper. It is a **MUST** prerequisite for any
Track-3 production resolver that claims a live graph:

1. **Validator-reachability repair** — members that are intentionally in the
   package must be reachable from declared entrypoints/form-fields (or the
   package must not pin them); the four MEMBER_UNREACHABLE defects on core are
   content/validator-graph debt.
2. **v1-generation content debt** — SCHEMA_NOT_ADMITTED / ROLE_MISMATCH /
   mapping fact-surface gaps on residual v1 citizens must be closed by admitted
   generations and correct pins so a production package can measure `ok=True`.

Until RG-1 is discharged for a package family, that family **must not** cross
the production `ok == True` gate. The gate itself is never relaxed to allowlist
the eight issues.

### 1.6 Consumed interlocks (not D3 discharges)

- **ADR-0031 (D1):** resolver reads candidates from residency `L` under the
  installed capability wall; no path copies live package bytes into a tracked or
  pushable artifact. Consumed, not re-proven; not a D3 “source isolation”
  discharge.
- **ADR-0032 (D2):** marshal-only `RunContext` and live-entrypoint kill-test remain
  Track-2/3 MUST conditions. D3 feeds only the exclusive graph into that future
  marshaller; it does not install it.

---

## 2. D3-P2 discharge / defer ledger

Disposition vocabulary (exactly one per row):

- **CS** — contract settled here (paper production-resolution contract)
- **PC(T)** — production condition; owner track T implements/proves
- **DEF** — deferred with reason (not silently partial)
- **N/A** — not applicable to D3 / expressly rejected elsewhere

### 2.1 ADR-0027

| Item | Disp. | Reason |
| --- | --- | --- |
| D1 package is sole membership unit | CS | Pins + release/registry authority; no path/`manifest.json` membership |
| D2 v2 member pin roles / role canon | PC(T4) | Fixture contract stands; production consumes same roles; not reopened |
| D3 admitted_schemas; no embedded schema-byte checksums | CS + N/A | Load rejects unadmitted schemas; embedded schema checksums remain **rejected** (ADR-0003 registry path) — not deferred as future work |
| D4 typed closed-graph validation | CS | Production requires `validate_package` outcome; graph only if `ok` |
| D5 form-field producer integrity | PC(T4) | Validator rule exists in fixture path; production inherits via ok gate |
| D6 package-instance immutability / registry-verified citizens | CS | Release-byte gate + registry entry verify + adoption package pin |
| D7 exclusive execution projection | CS | Pin-directed admission; unpinned inert; no partial graph |
| PC1 unpinned co-located inert | CS | Same-key filter never admits unpinned ids |
| PC2 conflict_semantics without producer → reject | PC(T4) | Contained in validate_package; production gate preserves reject |
| PC3 package+citizen checksums at pub/adoption | CS | Release→registry→package/member chain |
| PC4 issue-code strings are implementation detail | N/A | Behavior normative; codes non-normative |

### 2.2 ADR-0028

| Item | Disp. | Reason |
| --- | --- | --- |
| D1 versioned fact-type/bundle members | PC(T4) | Fixture contract; production resolves same citizens when pinned |
| D2 dual pin unit fact-type-bundle | PC(T4) | Same |
| D3 wholesale nested-set equality on adoption | PC(T4) | Bundle adoption acts remain Track-4/fixture obligation at bind |
| D4 mapping fact-type edges exact | PC(T4) | Enforced in validate_package when content is residual-closed |
| D5 composition_obligations package-declared | PC(T4) | Package field contract; not a resolver-location concern |
| D6 full composition binding per obligated symbol | PC(T4) | Validator |
| D7 mandatory quantity vocabulary | PC(T4) | Validator / content |
| D8 same-quantity force-declare | PC(T4) | Validator |
| D9 schema authority for obligation/pins | PC(T4) | admitted_schemas discipline |
| PC1 reject-direction goldens | PC(T4) | Content goldens; production gate does not weaken |
| PC1b accept/non-trigger goldens | PC(T4) | Same |
| PC1c confirmation readiness | N/A | Historical ratification record; not a live resolver condition |
| PC2 v1→v2 migration work | DEF | Migration of committed v1 bundles is implementation work outside D3 resolve shape |
| PC3 issue-code strings implementation detail | N/A | Same as 0027 PC4 |

### 2.3 Explicit non-rows (anti-laundering)

| Topic | Disp. | Reason |
| --- | --- | --- |
| ADR-0031 installed wall / gates | PC(T1/T3) | Consumed interlock; not D3 discharge |
| ADR-0032 marshal-only RunContext + kill-test | PC(T2/T3) | Consumed interlock; not D3 discharge |
| RG-1 reachability + v1-generation debt | PC(T3/T4) **MUST** | Prerequisite so production packages can measure `ok=True`; never allowlisted |
| Embedded schema-byte checksums | N/A | Rejected by ADR-0027 D3; do not reintroduce |

No ADR-0027/0028 named decision or PC above is left unclassified. **CS** means
the production-resolution *contract* is settled on paper; Track-3 still installs
the resolver. **PC(T)** means the fixture ADR already settled meaning and the
named track must still prove or migrate content. D3 does not claim Track-3/4
implementation complete.

---

## 3. Synthetic probe map (scratch `L`)

All probes use synthetic ids and a throwaway out-of-repo directory (ADR-0031 `L`).
Committed surfaces used read-only: `package_instance_checksum`,
`citizen_checksum`, `load_published_*_checksums`, `verify_published_package`,
`validate_package`, tax 2025 published registry, interest-slice and
core-calculations packages.

| # | Probe | Expect |
| --- | --- | --- |
| P1 | Release-byte replacement (forged release agrees with evil registry) | `RELEASE_BYTE_MISMATCH` |
| P2 | Registry forgery under honest release pin | `REGISTRY_BYTE_MISMATCH` |
| P3 | Package entry rewrite under honest registry | `PACKAGE_VERSION_REWRITE` / checksum mismatch |
| P4 | Competing user acts + automation act in same scope | selects unique current user act; automation ineligible |
| P5 | Stale user act alone vs with current | current wins when present; no caller override |
| P6 | Same-key honest+evil candidates, both enumeration orders | admits only registry checksum match |
| P7 | Evil-only same-key candidates | `MISSING_PINNED_BYTES` |
| P8 | Unpinned `demo.evil` co-located | absent from graph |
| P9 | Missing one pinned member | refuse; no partial graph |
| P10 | Member list reversed | identical graph set |
| P11 | interest-slice full chain | `ok=True`, graph admitted |
| P12 | core-calculations | `ok=False`, exactly eight issues; blocked by gate |
| P13 | Ledger completeness | every §2 row has exactly one disposition |

---

## 4. Track-3 install sketch (non-implementing)

When authorized: schemas for `release-registry.v1` and `act-package-adoption.v1`;
resolver entrypoint that performs §1 in order; hard `ok == True` gate; kill-tests
mirroring P1–P12; no merge of production resolver from this paper alone.

## 5. Stop

Stop at this Rung-2 paper boundary. New boundary triggers: any proposal to
weaken all-or-nothing validation, to let callers select registry/act/package
authority, or to allowlist RG-1 issues. Rung-3 (merged production resolver) is
out of charter.
---
**SEAL** — Iteration-3 clean-room rival deliverable `it6/design.md`. Held sealed
from incumbent until foreman custody. No implementation bytes.
