# D1 Real-Data Residency Boundary — Iteration 2 Rival Design

Status: clean-room rival, Rung-2 paper design plus throwaway probes. Scope is
D1-P1 and D1-P2 only. This document does not design contribution, package
resolution, new tax content, or a user interface.

## Contract anchors

The controlling boundary is Article 18 and the Ontology's definitions of
quarantine, sensitivity inheritance, and synthetic-by-default. A record that
describes a live workspace inherits that workspace's sensitivity. A fixture
whose provenance begins with an identifiable record is not synthetic, however
thoroughly its values were changed. E18.1 therefore requires a structural wall,
E18.2 requires an egress check, and E18.3 requires manufacturing provenance.
ADR-0030 C.8 adds the independent rule that a push is publication before any
remote-side check can run.

The current absolute-path test is a useful narrow detector, not the boundary:
it scans one fixture directory, has four textual markers, and has no commit or
push gate. The design below makes classification total, scans the complete
crossing envelope, and keeps the existing detector only as a regression check.

## D1-P1 — Residency, classification, and enforcement

### 1. Location rule

Let `R` be the union of every repository worktree, Git administrative directory,
object store, linked worktree, build output, publication cache, and remote. Let
`L` be a live workspace root chosen by the owner at bootstrap.

The versioned rule is:

1. `L` is selected at runtime under a declared quarantine root; no concrete
   locator, locator fragment, canonicalized path, hash of a path, or owner-local
   identifier is committed.
2. After canonicalization, neither `L` nor any descendant is in `R`, and no
   member of `R` is in `L`. Symlinks, hard links, junctions, bind mounts,
   submodules, alternates, and object-store indirection may not bridge them.
3. The ordinary authoring/publication environment has `R` read-write and no
   capability to read `L`. The live-run environment has the adopted code from
   `R` mounted read-only, `L` read-write, no repository write capability, and no
   publication/network capability. Run output, process records, ledgers, caches,
   and failures remain under `L`.
4. A run receives an explicit runtime capability for `L`; it does not discover
   a workspace from the repository, a committed config, the current directory,
   or an ambient environment default. The capability is local quarantine state.
5. Scratch is split by authority: public-development scratch is synthetic-only
   and cannot read `L`; live-run scratch is inside quarantine and cannot write
   `R` or publish.

A run may read the live workspace because it is a quarantine-serving pipeline
with an explicit capability. The repository cannot contain or indirectly reach
the workspace because it is mounted read-only into that pipeline and the
opposite publication environment has no live-workspace capability. This is a
directional structural wall, not an ignored-directory convention.

### 2. Complete binary classification

The unit classified is a **crossing artifact**: every byte and every item of
metadata that a commit, push, upload, API call, or generated publication would
make reachable outside quarantine. It includes content, names, paths, modes,
symlink targets, Git trees and metadata, ref and tag names, patch text, archive
members, PR text, logs, and attachments. A container never launders its members.

`classify(artifact)` returns exactly `MAY_CROSS` or `NEVER_CROSSES` by this
ordered rule:

1. If the artifact, any input to it, or anything it describes has personal
   provenance, classify `NEVER_CROSSES`. This includes live evidence, findings,
   values, identifiers, concrete locators, process records, ledgers,
   dispositions, summaries, excerpts, screenshots, hashes, encodings, and
   transformations. Sensitivity is monotone; there is no scrub or declassification
   operation.
2. If a seeded marker, private-locator form, personal-value sentinel, forbidden
   file type, hidden indirection, or contradictory provenance is detected,
   classify `NEVER_CROSSES`.
3. Otherwise, `MAY_CROSS` requires exactly one declared kind:
   - `code`: authored in the public-only environment from public or synthetic
     inputs;
   - `contract`: schemas, rules, governance, plans, ADRs, charters, reviews,
     process logs, retrospectives, and documentation authored only from public
     or synthetic inputs; or
   - `synthetic_fixture`: a manufactured fixture, golden, or test vector with
     the D1-P2 proof below.
4. A missing kind, missing proof, overlapping kind, unrecognized type, unknown
   origin, or unreadable member deterministically classifies
   `NEVER_CROSSES(reason = missing_may_cross_proof)`.

Thus uncertainty is a rejection reason, not a third class. A `.md`, `.py`, or
`.json` suffix is never proof. A contract may contain synthetic examples, but a
review derived from live dispositions is personal and never crosses even when
amounts are omitted. A run report stating which live lines published or blocked
describes the workspace and remains in quarantine; a public record may state
only that the owner performed the acceptance action and that no artifact crossed.

### 3. Versioned enforcement diff (paper)

The production change is represented at Rung 2 as this logical diff; no such
files are implemented in this iteration:

```diff
+ boundary-policy/v1.yaml
+   kinds: [code, contract, synthetic_fixture]
+   default: NEVER_CROSSES:missing_may_cross_proof
+   sensitivity: monotone
+   concrete_live_locators: forbidden
+   indirections: reject_unless_fully_materialized_and_scanned
+ boundary-policy/classification-attestation.schema.json
+ boundary-policy/synthetic-provenance.schema.json
+ tools/check_publication_boundary
+ .githooks/pre-commit
+ .githooks/commit-msg
+ .githooks/pre-push
+ tests/boundary/commit_kills/*
+ tests/boundary/push_kills/*
- fixture-only scan of packages/sample_data/kernel
+ whole crossing-envelope scan, with the fixture scan retained as regression
```

Each proposed index tree carries a versioned classification attestation for
every member other than the policy's canonical self-classified files. The
attestation binds the blob identity, declared kind, origin class, and required
synthetic proof. A gate rejects an absent, duplicate, stale, or contradictory
entry. The manifest is contract material and is itself scanned.

**Commit surface.** `pre-commit` scans the complete proposed index tree, not
only the diff: paths, regular blobs, modes, symlink targets, indirections, and
classification/provenance records. `commit-msg` scans the exact message and
trailers. A missing or wrong hook-policy version is a rejection. The supported
commit path invokes these gates before object creation; bypassing a gate is a
boundary violation, not an alternate workflow.

**Push surface.** `pre-push` consumes the exact local ref/object pairs supplied
to the transport. For every non-deletion ref it scans the entire reachable
commit graph, including every commit and tag message, tree entry, path, mode,
symlink target, blob, and classification/provenance record. It does not rely on
remote-tracking state, visibility, branch type, or a diff from `main`; new,
force-updated, and tag pushes receive the same check. Missing objects, parse
failures, or a policy-version mismatch reject. Transport is invoked only after
success. Remote CI repeats the scan as an audit backstop but cannot be the
privacy boundary because receipt already published the bytes.

Production must structurally install and integrity-check the hooks and ensure
remote credentials/transport are available only through the guarded push path.
That is a named production condition: a bypassable advisory hook alone does not
satisfy Article 18. The Rung-2 evidence settles the gate contract, not those
implementation bytes.

**Other publication surfaces.** Patch/bundle/archive creation and outbound API
payloads (including PR bodies, comments, and attachments) call the same
classifier before writing or sending. LFS and submodule publication are disabled
until their actual content and metadata are materialized into the envelope;
pointer-file scanning alone is insufficient.

### 4. Kill-test inventory

Every named surface has either a gate or a structural no-carry proof. The first
ten rows are the charter's mandatory enumeration; later rows close adjacent
container and platform paths.

| Surface | Potential carrier | Enforcement point or no-carry argument | Kill |
|---|---|---|---|
| Commit | worktree, index, message, tree, blob | full-index `pre-commit` plus `commit-msg`; default reject | personal-origin blob rejects before object creation |
| Push | reachable history, tags, refs, metadata | full-reachability `pre-push`; transport credential released only after pass | leak reachable only from a unit ref rejects and transport is not invoked |
| Test fixture | JSON/JSONL/text/binary test data | `synthetic_fixture` proof plus whole-envelope scan at commit and push | missing generator or personal-origin input rejects |
| Golden | expected output, explanation, snapshot | same proof; golden generator inputs must all be public/synthetic | live-run-derived golden rejects even with values removed |
| Charter | examples, paths, case descriptions | `contract` public-origin proof plus content scan | concrete live locator or personal example rejects |
| Review | quoted evidence and findings | same contract gate; live disposition detail is always personal | copied live status/value rejects; only non-descriptive action attestation may cross |
| Process log | incidents, commands, output | same contract gate; no live output or locator quotation | pasted live command/output rejects |
| Retrospective | verification and shipped evidence | same contract gate | live ledger excerpt or personal summary rejects |
| Scratch directory | editor temp, probe output, copied data | public scratch has no capability to `L`; live scratch remains inside quarantine with no repository/network write | synthetic marker proves public scratch; any bridge/mount fails topology audit |
| Run output / ledger | values, dispositions, explanations, failure records | created only below `L`; live-run environment cannot write `R` or publish | attempted output path outside `L` rejects before run; copied artifact rejects later gates |
| Concrete locator/config | local config, shell argument, history | locator is local quarantine state; run accepts a capability, not a committed path | committed locator form rejects |
| Link/mount/indirection | symlink, hard link, bind mount, Git alternate, gitlink, LFS pointer | canonical topology audit; opaque indirections default reject | target under `L` or unmaterialized content rejects |
| Git metadata | author text, commit/tag message, ref name | commit-message and full push-envelope scans | seeded personal marker in metadata rejects |
| Patch/bundle/archive | untracked export of tracked or untracked bytes | classifier runs over fully materialized members before creation | one never-crossing member rejects whole container |
| CI/cache/artifact | logs, caches, uploaded reports | CI has no live capability; synthetic-only inputs; outbound artifact gate | live canary is unreachable; seeded synthetic egress marker rejects upload |
| Terminal/log/telemetry/crash | stdout, shell history, traces, error reports | live terminal and logs are quarantine sinks; live runner has telemetry/network disabled | seeded live marker appears only inside quarantine sink |
| PR/remote metadata | body, comment, attachment, generated summary | outbound API payload gate before request | personal-origin or unknown-origin payload rejects before API call |
| Clipboard/manual copy | human-mediated text or file transfer | no automatic carry; anything pasted into a crossing artifact receives the same default-deny gates | pasted canary rejects at the next commit/push/API crossing |

### 5. Six Gate-2 cases and observations

All probes ran under a throwaway scratch root outside the repository. All names,
values, identifiers, paths, refs, and payers were synthetic. No Git command was
used. The push probe invoked the proposed hook logic directly over a synthetic
reachable-object envelope for `refs/heads/unit-demo`, consistent with the
Rung-2 ceiling and the no-Git-write stop condition.

| Case | Claim | Classification/enforcement change | Gate behavior | Observed result |
|---|---|---|---|---|
| 1. Clean boundary | disjoint residency permits an explicit live read without repository carry | topology rule plus public contract and synthetic-fixture proofs | accepts complete may-cross proof; public tree contains no live marker | exit 0; topology disjoint, explicit read succeeded, repository marker count 0; clean commit envelope accepted 2 artifacts |
| 2. Commit leak | personal provenance dominates a contract-looking path | full proposed-index classification | rejects before object creation with provenance reason | exit 42; `sensitive-provenance:personal`; transport not invoked |
| 3. Push leak | a commit-time bypass cannot make a reachable leak publishable | full reachable-object pre-push scan, independent of commit gate | rejects unit-ref envelope before transport | exit 42; `sensitive-provenance:live_run`; transport not invoked |
| 4. Synthetic derivation | public constraints can preserve declared shape without receiving live values | D1-P2 provenance proof and independent generator | accepts equal public shape with reserved synthetic namespace | exit 0; shape equal, forbidden-token overlap 0, origin public profile |
| 5. Ambiguity negative | unknown origin or a concrete locator is never an undecided state | fail closed to `NEVER_CROSSES` | rejects contract-looking config | exit 42; `sensitive-content-or-concrete-locator`; transport not invoked |
| 6. Kill enumeration | omission is mechanically detectable | required-surface set is versioned and checked | complete set accepts; deliberate omission rejects | 10-of-10 required surfaces accepted; version without `push` exited 43 and named `push` missing |

## D1-P2 — Synthetic re-expression without personal provenance

### 1. The rule

There is no real-document scrubber. A real document is never an input to a
repository fixture generator. Instead:

1. A public **shape grammar** is declared from public form specifications,
   repository schemas, and rule contracts. It may describe field names and
   types, ordering, schema-permitted presence, cardinality classes, source-family
   membership, closure topology, and cross-field constraints. It excludes
   observed strings, lengths of observed strings, amounts, dates, identifiers,
   payer identity, hashes, images, formatting accidents, and any feature whose
   only authority is a live document.
2. A public **profile catalog** or deterministic covering array is generated
   from that grammar. Profiles are identified by synthetic identifiers and exist
   independently of any owner document.
3. Inside quarantine only, a live document may be checked for coverage by an
   already-declared profile. The match, mismatch, selected profile, and reason
   remain inside quarantine because they describe the live document.
4. Repository fixtures are generated solely from the public grammar, a declared
   profile, a versioned generator, and a synthetic seed. All values come from
   reserved demo namespaces and constraint-driven synthetic domains.
5. If no public profile covers a live shape, no artifact crosses. The public
   grammar is expanded only from an independent public specification or a
   generally stated schema capability, then the catalog/covering array is
   regenerated without the live document. If that cannot be done, the case
   remains quarantined and unresolved.

This is a checkable re-expression: the repository instance is structurally
equivalent under a declared public projection, but causally independent of the
real values and record. The document can reveal a coverage defect inside
quarantine; it cannot supply the replacement fixture.

### 2. Required provenance proof

Every synthetic fixture and golden carries a manifest with:

- fixture and schema identifiers in a reserved synthetic namespace;
- generator identity/version and content digest;
- public grammar/profile identities and content digests;
- deterministic synthetic seed and value-domain constraints;
- declared cardinality, closure topology, and invariants exercised;
- an input-kind list limited to public contracts and constructed synthetic data;
- an attestation that no live workspace, evidence, finding, record, locator,
  captured output, or personal-derived intermediate was an input.

The gate recomputes the fixture from those pins and requires byte equality. It
also requires every textual identifier to use the synthetic namespace and runs
seeded-marker/value-overlap detectors as defense in depth. Missing provenance,
an extra input, a non-reproducible output, or a personal-origin edge classifies
the fixture `NEVER_CROSSES`.

The following are expressly invalid because their lineage still begins with the
record: replacing names, offsetting or rounding amounts, shuffling rows,
hashing identifiers, copying blank/nonblank patterns, preserving observed string
lengths, redacting a ledger, or asking a model to rewrite a live document.

### 3. Rung-2 evidence and limits

The throwaway probe used a synthetic quarantine canary document and a separately
authored public profile. The generator received only the public profile, produced
a fixture with the same declared field/cardinality/closure projection, used a
reserved demo namespace, and had zero overlap with the canary payer, identifier,
or values. This establishes the rule's non-carry shape at Rung 2.

Production still must implement the policy schemas, topology/capability audit,
complete-envelope gates, guarded transport, reproducible generator, provenance
checks, and kill tests. Remote privacy, ignored paths, textual scanning alone,
and a reviewer promise are never load-bearing.

## Conclusion

D1-P1 and D1-P2 are both settled at Rung 2 as contract shapes. The result is a
directional structural quarantine, a total fail-closed binary classifier, commit
and independently probed push gates over complete envelopes, a complete named
kill inventory, and an independent-construction rule for real-shaped synthetic
coverage. Implementation remains a production condition of the milestone; no
enforcement code, tests, fixtures, or scans were changed here.
