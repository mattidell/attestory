# ADR 0031 — Real-Data Residency Boundary

- Status: **accepted** (owner ratification 2026-07-16, PR #3, merge `ce86525`). The scoped confirmation pass on Decision 5 ran and its named amendment was applied (see Confirmation pass outcome) before ratification.
- Tier: 3
- Date: 2026-07-16

## Context

The First Real Return Slice crosses the synthetic boundary: the owner's real
tax data enters a live workspace for the first time. D1 is the milestone's
data-residency contract — where live data lives and what may ever cross into the
repository or any remote. The failure mode is **irreversible**: a leak cannot be
unleaked, and ADR-0030 §C.8 (ratified) makes a push publication regardless of
repo visibility, so the boundary must hold on the push surface and the interim
private-remote posture must never be load-bearing.

The pre-D1 floor was one narrow test
(`test_committed_kernel_fixtures_have_no_absolute_local_paths`): four path
markers over one directory, no git hooks, no push guard.

The D1 prototype (branch `decision/d1-real-data-residency`, plan
`docs/archive/2026-08-02-milestone-artifacts/prototypes/real-data-residency/plan.md`) produced two clean-room-separated
Rung-2 paper builds — incumbent (`it1/design.md`, `examination-it1.md`) and
rival (`it2/design.md`, `examination-it2.md`) — and two independent committee
reviews (`reviews/governance-r1.md` Medium, `reviews/adversary-r1.md` High).
**Both reviewers independently converged:** the rival design survives at Rung 2;
the incumbent carries decision-blocking gaps on three axes the rival resolves
(push independence, sensitivity inheritance, locator model), plus a
decision-blocking D1-P2 shape-channel leak. This ADR ratifies the rival basis on
those axes and the both-agreed contracts, and records the residuals and
production conditions the committee named.

A governance defect surfaced by the Governance review (M4) was reconciled by the
owner (2026-07-16): the milestone plan's Verification wording ("the report —
dispositions, not values — is what reviews cite") conflicted with Ontology §8
sensitivity inheritance. **Ontology governs**; the milestone plan is corrected by
version (disposition detail stays quarantined; only a non-descriptive attestation
crosses). Decision 7 records the boundary that rests on.

## Decision

1. **Residency is a rule, not a path (directional capability wall).** A live
   workspace `L` is chosen by the owner at bootstrap; the rule constrains only
   `L`'s *relation* to the repository, never its bytes. After canonicalization,
   neither `L` nor any descendant is inside any repository worktree, git store,
   linked worktree, build output, publication cache, or remote, and no such
   surface is inside `L`; no symlink, hard link, bind mount, submodule, or
   object-store alternate may bridge them. The ordinary authoring/publication
   environment has **no capability** to read `L`; a live run receives an explicit
   runtime capability for `L`, mounts repository code read-only, writes only
   inside `L`, and has no publication/network path. This is why a run may read
   live state while the repository provably cannot contain or reach it
   (Constitution Article 18; the incumbent's ignored-directory framing is
   rejected — see Rejected).

2. **Classification is a total, fail-closed binary function.** Every crossing
   artifact — every byte and metadata item a commit, push, upload, API call, or
   generated publication would make reachable outside quarantine (content, paths,
   names, modes, symlink targets, trees, commit/tag messages, ref names, patch/
   archive members, PR/API text) — classifies to exactly `MAY_CROSS` or
   `NEVER_CROSSES`. `MAY_CROSS` requires exactly one proven kind: public-origin
   code, public-origin contract, or independently-constructed synthetic fixture
   (Decision 6). Missing, conflicting, unknown, overlapping, or unreadable proof
   is itself a deterministic `NEVER_CROSSES` reason. There is **no undecided
   class** — uncertainty is a rejection, not a third outcome. (Committee: both
   builds total and fail-closed, probed at Case 5; totality unbroken by the
   adversary.)

3. **Enforcement is commit + an independent push gate over the whole envelope.**
   The commit gate classifies the full proposed index tree plus the message. The
   push gate is **independent of the commit gate and of remote-tracking state**:
   for every outgoing ref it scans the entire reachable object graph — commits,
   trees, blobs, commit *and tag* messages, ref names, modes, symlink targets —
   and does **not** rely on remote-tracking refs, visibility, branch type, or a
   diff from `main`. (Resolves ADR-0030 §C.8. The incumbent's
   `rev-list --not --remotes` scoping is rejected: it keys on remote state and
   excludes already-pushed-reachable commits from re-scan.) Remote CI repeats the
   scan as an **audit backstop only** — receipt is already publication, so CI can
   never be the privacy boundary.

4. **No locator is committed, in any form.** The repository contains no residency
   path, path fragment, canonicalized path, hash of a path, or owner-local
   identifier — not in tracked content and not in an ignored pointer file. The
   run receives the locator as runtime capability state. (The incumbent's
   ignored-root pointer file is rejected as a load-bearing ignore under Article 18
   / Ontology §8.)

5. **Locator content screen targets owner-local-resolvable forms, as
   defense-in-depth over Decisions 4 and 2.** *(Foreman-authored refinement
   closing Adversary A2; amended per the confirmation pass — see Confirmation
   pass outcome. Now ratifiable.)* The residency screen rejects a
   **private-locator / owner-local-resolvable** token — one that could resolve to
   the residency root `L` — not every absolute-path string; public system, CI,
   and container roots are out of the residency screen's scope (governed, if at
   all, by their own kind and by Decision 2 rule 1 provenance). The screen must
   not depend on the runtime locator value to be complete, so a fresh clone or CI
   enforces the same rule. **Declaration privilege (structural, not
   class-judgment):** a `contract`- or `code`-kind artifact may contain a
   denied-form token only if that token is a member of a **declared reserved
   illustration domain** — a fixed, non-resolvable enumeration of example forms
   that is itself part of the permitted grammar; any token outside that set still
   denies regardless of kind, so a resolvable owner-local path can never ride in
   as an "example." This licenses quoted *forms*, never a live locator, and does
   not weaken the fresh-clone under-inclusion guard (a novel real root is not a
   member). Primary walls remain Decision 4 (no committed locator) and Decision 2
   rule 1 (provenance); this form screen is defense-in-depth over them. (Replaces
   the incumbent's fixed 3-prefix denylist, which a novel root evades.)

6. **Synthetic fixtures are independently constructed, never sanitized.** A real
   document is **never** an input to a repository fixture generator. A public
   **shape grammar** is declared only from public form specifications, repository
   schemas, and rule contracts; it excludes observed strings, observed string
   lengths, exact observed cardinalities, observed closure topologies, and any
   feature whose sole authority is a live document (it uses **cardinality
   classes** and a public covering array). Inside quarantine a live document may
   only *select* an already-public profile; the match and selection never cross.
   Repository fixtures are generated from the public grammar + a declared profile
   + a versioned generator + a synthetic seed, from reserved demo value domains.
   Every fixture/golden carries a provenance manifest (generator id/version+digest,
   grammar/profile digests, seed, constraints, input-kind list, and an attestation
   that no live/personal-derived input was used); the gate **recomputes the
   fixture from the pins and requires byte equality**, and runs value-overlap
   detectors as defense in depth. Rename/offset/shuffle/hash/redact/model-rewrite
   of a real document are expressly invalid — provenance beginning with an
   identifiable record is not synthetic (Ontology synthetic-by-default; discharges
   E18.3's recorded debt). (Rejects the incumbent's extract-then-fill, which leaks
   observed field names, exact cardinality, and closure topology as "shape" —
   Adversary A4.)

7. **Sensitivity is inherited by description (Ontology §8).** An artifact with
   personal provenance **or that describes personal material** classifies
   `NEVER_CROSSES` — including live evidence, findings, values, identifiers,
   locators, process records, ledgers, dispositions, summaries, and excerpts. A
   live-run **disposition report** is quarantined even with amounts removed; only
   a **non-descriptive attestation** (that the owner performed the run, that
   dispositions were observed in quarantine, and that no artifact crossed) may
   cross. (The content-screen-only incumbent classifier, which passes a review
   describing a real run, is rejected. This is the boundary the milestone plan's
   corrected Verification section rests on.)

8. **Named residuals (not blocking; recorded for D2/implementation).** (a) A
   `git add` stages a loose object and index entry with no gate until commit/push;
   this is local-only, inside the owner trust boundary, with no remote carry —
   acceptable, flagged for the implementation's local hygiene. (b) The
   coverage-expansion decision log (Decision 6 — the record of which public
   profiles were added after a live session) must itself stay in quarantine, as
   the *pattern* of additions describes the live document (Adversary A5). (c) The
   D1 topic's own establishing evidence (this ADR, the charters, the builds, and
   the committee reviews) quotes denied path forms as illustrations. The reserved
   illustration domain (Decision 5) is declared to include the example forms
   already used in the topic's evidence as of ratification, so the boundary is
   consistent with its own record; the delivered committee reviews are **not**
   rewritten (record integrity). Track 1/3 implements the reserved domain and the
   enforcement together.

## Production conditions (discharged in milestone Tracks 1/3, per ADR-0027/0028 pattern)

This ADR settles the **contract** at Rung 2; the following are named production
conditions, not part of the Rung-2 claim, to be discharged and re-verified in
implementation: the whole-envelope classifier and commit/push gates as installed,
integrity-checked hooks that a run entrypoint structurally requires; **guarded
transport** — remote credentials reachable only through the guarded push path, so
raw `git push`/`--no-verify` cannot bypass the gate (Adversary A3; the incumbent's
CI-detection + remote purge-and-rotate is rejected as load-bearing since §C.8
publication cannot be un-published); the reproducible synthetic generator and
byte-regeneration provenance check; topology/capability audit (E18.1 canary); and
the kill-test suite over the enumerated surfaces (E18.2 seeded-marker).

## Confirmation pass outcome (Decision 5)

Decision 5 is a foreman-authored fix closing an adversary under-inclusion finding
(prefix denylist under-catches). Per ADR-0013 (2026-07-15) it ran a scoped
confirmation pass exercising the **opposite** direction, over-inclusion
(`reviews/confirm-locator-screen.md`, Medium). The pass **found an over-fire**: a
form-only allow-list denies legitimate `contract`/`code` content that merely
*quotes* a denied path form — acutely, this ADR's own text and the D1
charters/reviews would be rejected by the rule they establish. The reviewer named
a minimal, both-directions-checked amendment — re-scope the screen to
owner-local-resolvable forms, and add a **structural** reserved-illustration-domain
declaration privilege — and verified the under-inclusion fix (Case 5) stays closed.
Decision 5 above is amended accordingly; residual 8(c) records the consequence for
the topic's own evidence. Because the amendment was **designed and
both-direction-checked by the reviewer** (not authored unchecked by the foreman),
it satisfies the ADR-0013 guard without a further confirmation pass. Decision 5 is
now ratifiable.

## Consequences

- Real data has a ratified boundary: an out-of-repo residency by rule, a total
  fail-closed classifier, independent commit/push envelope gates, no committed
  locator, independent-construction synthetic fixtures, and description-level
  sensitivity — the substrate D2 (contribution) writes into and D3 (resolver)
  reads from.
- The pre-D1 narrow scan becomes a regression check inside a whole-envelope gate.
- The milestone's in-repo acceptance evidence is a non-descriptive attestation;
  disposition detail lives only in quarantine.
- E18.3's recorded debt is discharged by the manifest + byte-regeneration check.

## Rejected (incumbent it1 positions, per committee)

- **Push scan keyed on remote-tracking state** (`rev-list --not --remotes`) —
  violates §C.8 push independence (Governance M2).
- **Content-screen-only classification** — cannot inherit sensitivity to
  description-bearing artifacts (Governance M4, Ontology §8).
- **Ignored-root pointer file + prefix-denylist locator screen** — a load-bearing
  ignore that a novel absolute root evades on a fresh clone (Governance M6,
  Adversary A2).
- **Extract-then-fill synthetic derivation** — leaks observed field names, exact
  cardinality, and closure topology as shape (Adversary A4).
- **CI-detection + remote purge-and-rotate** as the push backstop — treats the
  remote as a safety net §C.8 forecloses (Adversary A3).

## Links

- Prototype plan: `docs/archive/2026-08-02-milestone-artifacts/prototypes/real-data-residency/plan.md`
- Builds: `it1/design.md` + `examination-it1.md` (incumbent); `it2/design.md` + `examination-it2.md` (rival)
- Charters: `charter-it1.md`, `charter-it2.md`, `charter-review-governance.md`, `charter-review-adversary.md`
- Committee: `reviews/governance-r1.md`, `reviews/adversary-r1.md`; triage in `process-log.md`
- Contracts: Constitution Article 18; Engineering Constraints E18.1/E18.2/E18.3; Ontology §8 (quarantine, sensitivity inheritance, synthetic-by-default); ADR-0030 §C.8
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/first-real-return-slice.md` (Verification corrected 2026-07-16)
- Process: extends ADR-0005/0013 (prototype economic gates); interlocks with D2 (contribution) and D3 (production resolver), separate ADRs
