# D3 it2 — Production Package Resolver (Clean-Room Rival Design)

Builder: clean-room rival, High tier, independent context (charter-it2.md).
Date: 2026-07-16. Rung 2: paper diffs + throwaway probes against the committed
loader/validation/runner and a scratch out-of-repo workspace `L`. No resolver
code merges; the fixture path is untouched.

**Seal statement.** This design was derived only from: the repository entry
chain, `plan.md`, `charter-it2.md`, `docs/governance/`, ADR-0027/0028/0031
(plus ADR-0032's decision list for the interlock), the committed
`packages/derivation/` loader/validation/runner/marshal sources, the
`artifact-package.v2` schema, and the committed synthetic content fixtures.
No incumbent material (`it1/`, `examination-it1.md`) was read.

## 1. Actors and the one framing decision

A production run has three byte populations with different trust:

1. **The repository content mount** — ratified public content (packages,
   member citizens, publication registries, published schemas), mounted
   read-only into the live-run capability (ADR-0031 decision 1).
2. **The live workspace `L`** — the owner's record (act log, facts,
   contributions per ADR-0032) plus whatever content bytes happen to be
   present there. Everything in `L` is *untrusted supply* until verified.
3. **The publication registries** — `published-packages.json` (package
   instances + citizen checksums) and the schema registry `published.json`.

The framing decision, from which the rest follows: **authority is
registry-resident; location is only supply.** ADR-0027 d6 already says
"resolution trusts registry-verified content, not bare id/version string
equality against arbitrary corpus bytes." The production resolver takes that
literally: it does not matter *where* candidate bytes for a pinned member are
found — repo mount or `L` — because admission requires byte-equality with the
repo-resident registry checksum. A byte-verified copy is *the* published
citizen wherever it sits; unverifiable bytes are nothing, wherever they sit.

## 2. D3-P1 — The production resolution contract (decisions R1–R8)

**R1. Trust anchor is repository-resident and never read from `L`.** The
package registry, citizen checksum registry, and published schema set are read
only from the read-only repo mount. `L` can therefore never rewrite its own
trust anchor: a workspace that tampers with a local registry copy changes
nothing, because no local registry copy is ever consulted.

**R2. Adoption locates; paths never do.** The resolver's input naming *which*
package(s) to resolve is the adoption record in `L`'s act log — exact
`(package_id, version)` pins, the same adoption-pin shape the fixture path's
scenarios carry. No directory walk, filename convention, config file, or
environment variable is adoption authority (ADR-0027 d1). A missing or
ambiguous adoption record is a typed refusal, not a default.

**R3. Supply is source-indifferent and checksum-arbitrated.** For the adopted
package and for each member pin `(id, version)`, the resolver gathers candidate
bytes from its supply sources (repo content mount; `L`'s content store).
Admission per key: the candidate set is filtered to bytes whose canonical
checksum equals the registry entry for that key. Exactly one distinct verified
byte-content may survive (verified duplicates collapse to one member).
Consequences, both directions:
- *No verified candidate* → `MEMBER_BYTES_UNAVAILABLE`, refuse (fail-closed).
- *Unverified candidates present* (impostors, junk, drafts) → inert. Their
  presence cannot shadow, poison, or displace a verified copy, and cannot make
  an unverified copy load. Presence of junk is never an error; absence of
  verified bytes always is.

**R4. Verification is total and ordered: instance first, then every member.**
Step one verifies the package instance itself — recorded `package_checksum`
recomputed over canonical bytes, then compared to the registry pin
(`verify_published_package` semantics: missing field, recomputed-field rewrite,
unpublished instance, and registry divergence are four distinct rejects). Step
two verifies **every** member pin under R3 plus schema validation against the
published schema set. In the committed fixture validator the citizen-checksum
registry is an *optional* parameter (`published_citizen_checksums: ... | None`);
in the production entrypoint it is **mandatory** — there is no signature by
which a production caller can skip byte-verification.

**R5. The gate is all-or-nothing; refusal is typed and recorded in `L`.**
Production resolution succeeds only when validation returns **zero issues**
(`ok == True`). There is no contained-issue leniency: no partial graph, no
"proceed and record" (that posture is correct for fixture-path migration
tooling and goldens, wrong for a production run). A refusal is a typed outcome
carrying the full issue list, written as a quarantined ledger artifact inside
`L` — never printed into a tracked file, never an unhandled exception. Probe
P3a shows the committed path currently dies with a raw `KeyError` when a
mutated member is excluded mid-pipeline; the production contract forbids that
failure mode: the gate refuses *before* any run state is constructed.

**R6. Exclusive projection is pin-directed and deterministic.** The corpus
offered to validation is constructed only by pinned-key lookup under R3 — the
resolver never enumerates a directory to decide membership, so a co-located
unpinned file is structurally unreadable by resolution, not merely filtered
later. The resolved member graph is projected into run inputs exactly as the
fixture path does (rules/parameters/families/mappings/fact-types from
`validation.resolved_members`; `input_bindings` from the package), feeding the
sole marshal-constructed `RunContext` (ADR-0032 decision 3 interlock).
Determinism note from probe P2b: the fixture loader's corpus glob is
**unsorted**, so a same-key co-located impostor wins or loses by filesystem
enumeration order. Registry checksums catch the swap either way, but the
production contract additionally removes the race: pin-directed lookup has no
enumeration order to depend on.

**R7. D1 interlock — consumed, not re-proven.** The resolver runs inside the
ADR-0031 run capability: repo mounted read-only (structural — no write path
exists), all writes confined to `L`, no publication or network path. Its
outputs — the resolved graph handle, the run inputs, and the refusal ledger —
are workspace artifacts that classify `NEVER_CROSSES` by description
inheritance (ADR-0031 decision 7), even though verified content bytes are
public: *which* package the owner resolved, *when*, and *with what outcome*
describes the owner's live activity. Only the non-descriptive attestation
crosses. The resolver adds no new crossing surface, so it cannot weaken the
wall; the commit/push envelope gates (ADR-0031 decision 3) remain the wall.

**R8. Strict superset by construction, plus a parity golden.** The production
path calls the *same* committed validator — one code path, not a sibling —
with strictly more mandatory inputs (citizen checksums required; instance
verification required) and a strictly stricter gate (`ok == True` required vs.
ignored). Every fixture-path guarantee is therefore present verbatim, and four
guarantees are added:

| Guarantee | Fixture path today | Production path |
|---|---|---|
| Member schema validation | yes (contained) | yes (gated) |
| Member byte-verification | optional parameter | mandatory |
| Package-instance verification | fixture-runner calls it | mandatory, first |
| Issues block execution | **no** (`ok` ignored; probe P1) | yes, all-or-nothing |
| Corpus admission | unsorted glob, last-writer-wins | pin-directed, deterministic |
| Co-located unpinned file | read into corpus, excluded from graph | never read by resolution |
| Failure mode on bad member | uncontained `KeyError` (probe P3a) | typed refusal, recorded in `L` |
| Trust anchor | fixture-relative registry path | repo-resident only, never `L` |

## 3. Paper diffs (versioned, no code merged)

- **New module (Track 3): `packages/derivation/production_resolver.py`** with
  one entrypoint, sketched contract:
  `resolve_production(adoption: AdoptionRecord, supply: SupplyIndex, anchor: TrustAnchor) -> ResolvedGraph | Refusal`.
  `TrustAnchor` wraps repo-resident registries + schemas; `SupplyIndex` wraps
  pinned-key candidate lookup over the repo mount and `L`; `Refusal` carries
  the typed issue list and is what the quarantined ledger records. `ResolvedGraph`
  is the only object from which the marshal-only `RunContext` constructor
  (ADR-0032) accepts content.
- **`package_validation.py`: no behavioral change to the shared checks.** One
  additive change: a production-entry wrapper (or keyword `require_clean=True`)
  that makes `published_citizen_checksums` non-optional and converts any issue
  into `Refusal`. The permissive signature remains for fixture/migration tools.
- **`runners/derive.py`: unchanged.** It stays the fixture-path reference.
  (Its unsorted glob and `ok`-ignoring leniency are recorded as fixture-path
  facts RG-2/RG-3 below; repairing them there is optional Track-3 hygiene,
  not part of this contract.)
- **No schema changes.** `artifact-package.v2`, the registries, and the
  published-schema pattern (ADR-0027 d3: no embedded schema-byte checksums)
  are consumed as-is.

## 4. The six cases (claim → change → behavior → observed)

All probes ran against the committed machinery, read-only, with the committed
synthetic `tax.us.2025.package.core-calculations` (44 pins) staged into a
scratch out-of-repo `L` (session scratchpad), driving the committed
`derive` runner and `validate_package` directly. Probe script was throwaway.

**Case 1 — clean production resolution with fixture parity.** Claim: the same
adopted package resolved from `L` yields the same resolved graph and run
report as from the committed fixture. Change: none (staging only). Behavior:
R2–R6 resolve and a run executes. Observed: the committed runner on the
`single_standard_deduction` scenario staged in `L` produced a **byte-identical
JSON report** to the repo-fixture run (P1: `byte_identical_report: true`;
17 published symbols; deterministic content-addressed finding ids make the
comparison exact). Direct validation resolved 44/44 pins. **Finding RG-1:**
the committed package validates with `ok == False` — seven pre-existing
contained issues (`ROLE_MISMATCH`/`SCHEMA_NOT_ADMITTED` on the v1 W-2 rule,
`MAPPING_FACT_TYPE_NOT_ADMITTED` on one mapping, four `MEMBER_UNREACHABLE`
including the `optional_default` parameters, which looks like a validator
reachability-edge gap rather than content debt). The fixture runner ignores
this and publishes. Under R5 the production gate would **refuse today's
committed package** — which is the honest fail-closed answer, and creates a
named Track-3 obligation (§6) rather than a leniency carve-out.

**Case 2 — exclusive projection: co-located unpinned file inert.** Claim: an
unpinned file in `L` is not executable or renderable. Change: a synthetic
unpinned `rule-artifact.v2` publishing a novel symbol written into `L`'s
content directory. Behavior: under R6 resolution never reads it. Observed
(P2a): the fixture glob *does* read it into the corpus (`in_corpus: true`),
but it never enters the resolved graph (`in_resolved_graph: false`) and the
run report is unchanged. The fixture path holds d7 at the projection layer;
the production path holds it one layer earlier (never read). Supplementary
(P2b): a co-located **same-key impostor** (same `(id,version)` as a pinned
member, different bytes) races the real file in the unsorted glob — in the
sorted-order probe it shadowed the member and byte-verification caught it
(`MEMBER_CHECKSUM_MISMATCH`); in the runner's enumeration order it happened to
lose and was silently inert. Registry arbitration (R3) removes the race.

**Case 3 (mandatory) — byte-verification fail-closed, both probes.** Claim: a
member whose bytes mismatch its registry checksum, and a package instance
whose bytes mismatch, both reject at load. Change: (a) one member's bytes
mutated in `L` (description edit); (b) the package instance's scope mutated,
probed with a stale `package_checksum` and again with the checksum field
recomputed. Observed: (a) `MEMBER_CHECKSUM_MISMATCH` on the mutated member
(P3a) — and the committed runner then **crashed uncontained** (`KeyError` on
the excluded parameter, exit 1): fail-closed in effect, but not typed; R5
converts this into a recorded refusal. (b) `PACKAGE_CHECKSUM_MISMATCH` for the
stale field and `PACKAGE_VERSION_REWRITE` for the recompute-the-field attack
(P3b) — both raised before any member work, matching R4's order. Nothing
published in any mismatch probe: fail-closed, not fail-open.

**Case 4 — D1 interlock, no leak via resolution.** Claim: resolution never
copies live content into a tracked or pushable artifact. Change: none —
structural argument under R7 plus probe hygiene. The resolver's write surface
is `L` only; the repo mount is read-only inside the run capability, so a
resolver that tried to write a tracked artifact has no path to do so; anything
that somehow crossed would still face the ADR-0031 commit/push envelope gates
and description-inheritance classification (a resolution ledger *describes*
the owner's run → `NEVER_CROSSES`). Observed: after all probes, `git status`
over the repository shows no change beyond this topic's two authored documents;
every probe artifact lives under the out-of-repo scratchpad. D3 consumes the
wall; nothing here re-proves or weakens it.

**Case 5 — negative: no silent partial load.** Claim: a package missing a
pinned member rejects rather than partially resolving. Change: one pinned rule
(`rule.form1040-line16`) deleted from `L`'s supply. Observed (P5):
`MEMBER_ABSENT` plus cascade issues (`FORM_FIELD_BINDING_MISSING`,
`MEMBER_UNREACHABLE` on the orphaned parameter); the committed runner exited 1
(uncontained) — nothing published, so no silent partial *result*, but the
refusal is again untyped. R5 makes the reject a first-class recorded outcome.
Under R3 the same refusal fires as `MEMBER_BYTES_UNAVAILABLE` even when junk
candidates for that key are present but unverifiable.

**Case 6 (mandatory) — discharge/defer ledger.** §5, in full.

## 5. D3-P2 — Discharge/defer ledger (every named ADR-0027/0028 condition)

"Discharged (contract)" = settled by this Rung-2 contract, re-verified in
implementation; "carried" = fixture-path check runs verbatim inside the
production gate (R8, one code path); "deferred" = explicitly not discharged
here, with owner and reason. No item is silently partial.

| # | Named condition | Disposition |
|---|---|---|
| 0027 d7 | Exclusive execution projection beyond fixtures | **Discharged (contract)** — R6; probed case 2 |
| 0027 PC1 | Golden: co-located unpinned file inert after adoption | **Discharged (contract)**; implementation golden owed by Track 3 |
| 0027 PC2 | Conflict semantics without selectable producer → reject | **Carried** — same validator inside the R5 gate |
| 0027 PC3 | Package-instance checksum at adoption; members via registry | **Discharged (contract)** — R4 makes both mandatory; probed case 3 |
| 0027 PC4 | Issue-code strings are implementation detail | Acknowledged — behavior normative, codes free |
| 0027 d3 | `admitted_schemas` rejection; no embedded schema-byte checksums | **Carried** (probed: `SCHEMA_NOT_ADMITTED` fires); embedded checksums **stay rejected** — schema bytes remain the ADR-0003 registry's job, repo-resident per R1 |
| 0027 N1/N2 | Fact-surface + composition trigger | Closed by ADR-0028; carried below |
| 0028 PC1 | Reject-direction goldens (force-declare, quantity-mandatory, orphan pin…) | **Carried** — mechanisms run inside the gate; golden-fixture inventory **deferred to Track 4** (coverage work, not contract) |
| 0028 PC1b | Accept-direction non-trigger goldens (cross-quantity) | **Carried**; inventory deferred to Track 4 (same reason) |
| 0028 PC1c | Confirmation status | N/A — already discharged pre-ratification |
| 0028 PC2 | v1→v2 bundle/fact-type migration | **Deferred to Track 3/4** — now *load-bearing*: RG-1 shows the committed package carries v1-generation debt the R5 gate will refuse |
| 0028 PC3 | Issue-code strings | Acknowledged, as 0027 PC4 |
| 0031 production conditions | Gates-as-installed, guarded transport, generator, canary, kill-tests | **Deferred to Tracks 1/3 (already owed there)** — consumed via R7, not D3's to discharge |
| 0032 MUST condition | Marshal-only `RunContext` constructor + kill-test | **Deferred to Track 2/3** — interlock honored: `ResolvedGraph` is the sole content feed to that constructor (R6) |

**New obligations surfaced by this round (named, not absorbed):**
- **RG-1** — bring the committed package to `ok == True` before first
  production run: repair the validator's missing reachability edge for
  `optional_default` parameters (defect, Tier 1), and clear the v1 W-2 rule
  generation + mapping fact-surface debt (content work, with 0028 PC2). The
  gate does not bend to meet the package; the package rises to meet the gate.
- **RG-2** — fixture loader corpus glob is unsorted (nondeterministic
  same-key admission); production path avoids it structurally (R6); optional
  fixture-side hygiene fix.
- **RG-3** — mismatch/absence currently surfaces as an uncontained `KeyError`
  in the runner; production refusals must be typed and ledger-recorded (R5).

## 6. Divergence and convergence signals for committee

Independently derived; where the incumbent lands elsewhere, the likely
contested axes are: (a) registry/trust-anchor residency (R1 forbids any
`L`-resident registry copy); (b) all-or-nothing gating with **no** leniency
carve-out despite RG-1 refusing today's committed package; (c) supply
indifference under checksum arbitration (R3) versus a designated single
content home; (d) pin-directed corpus construction versus enumerate-then-
filter. Each is argued above from ADR-0027 d6/d7, ADR-0028's fail-closed
posture, and ADR-0031's capability wall.
