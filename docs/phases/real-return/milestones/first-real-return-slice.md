# Milestone: First Real Return Slice

Status: **proposed** (2026-07-15) — awaiting owner plan approval before any
charter (ADR-0013). First milestone of the Real Return phase; operates under
ADR-0030 per-ADR / per-track merges (no monolithic milestone branch).

## Decision summary (tiered)

- **Tier 3 (owner, prototype-backed):** D1 real-data residency boundary — where
  live workspaces live, what may ever enter the repository, and how synthetic
  fixtures are derived from real shapes. Product-visible and irreversible in
  its failure mode (a leak cannot be unleaked).
- **Tier 3 (owner, prototype-backed):** D2 contribution boundary — how a real
  document's numbers become facts: contribution as a product event distinct
  from runs ("runs consume facts, not inputs"), manual entry as the first
  ingestion mode, user-facing vocabulary ("contribute").
- **Tier 2 (default + veto, prototype-backed):** D3 production package
  resolver — resolution beyond the fixture boundary (named deferral of
  ADR-0027).
- **Tier 1 (log only):** W-2 closure-mapping content under existing ADR-0014;
  live-run harness mechanics.

## Objective

The owner's actual W-2 and 1099-INT facts enter a live workspace through a
contribution boundary, resolve through a production package resolver, and
produce the owner's real Form 1040 lines **1a, 2b, 9, 11, 12, 15, 16** with
full explanations — while the repository provably continues to carry **zero
personal data**. Everything Foundation built becomes user value for the first
time.

## Why this milestone

Foundation's closing maturity read: computation/record aspects are uniformly
at synthetic maturity (L2), while the data-boundary aspect is absent (L0). No
further coverage breadth or presentation work changes what the product does
*for its user* until real data can enter. The data boundary is also itself
contract-foundational — better ratified before coverage widens than retrofit
across more content. Selected by the owner 2026-07-15 over coverage breadth
(dividends/Schedule B), a presentation surface, and deferral hardening.

## Current state

- Lines 1a/2b/9/11/12/15/16 flow end-to-end on synthetic fixtures with honest
  blocking, byte-verified packages, a run-disposition ledger, and walkable
  non-publication explanations.
- All data is synthetic (`demo-*`); fixture-safety tests in the suite
  (`tests/test_kernel_fixtures.py`) enforce this inside the repo, but nothing
  defines where *real* data may live. The repository has a GitHub remote
  (private for now, per the ADR-0030 amendment's interim posture), so the
  safety contract must treat every push as publication regardless of
  visibility.
- Package resolution exists only inside the fixture boundary (ADR-0027
  deferral).
- The W-2 family has no closure mapping: an empty W-2 set blocks, and there is
  no way to declare "these are all my W-2s."
- Facts are asserted through kernel member transitions; there is no
  contribution-level product event recording *how* a batch of real inputs
  became facts.

## Scope

1. **Real-data residency contract (D1).** Live workspaces live outside the
   repository at a declared location; a data-classification rule states what
   may cross into the repo (nothing personal — code, contracts, and synthetic
   fixtures only); the mechanized safety check extends to whatever new surface
   the boundary creates.
2. **Contribution boundary (D2).** A contribution event turns manually entered
   real document values into facts with provenance; runs consume facts, never
   inputs. Manual entry only — no document parsing/OCR.
3. **Production package resolver (D3).** Adopted packages resolve outside the
   fixture boundary with the same exclusive-projection and byte-verification
   guarantees (ADR-0027/0028 production conditions).
4. **W-2 closure mapping.** Content under existing ADR-0014 so a real W-2
   family can close and line 1a can publish.
5. **Live-run verification.** A repeatable way for the owner to run the slice
   against the live workspace and see published/blocked dispositions with
   explanations, using existing output surfaces (no new UI).

## Non-goals and deferred boundaries

- **No document parsing/OCR** — manual entry is the ingestion mode.
- **No new tax lines or forms** — dividends, Schedule B, and other coverage
  stay on the matrix frontier for a later milestone.
- **No human presentation surface** — E8.1 and citation display remain
  deferred; existing CLI/JSON output surfaces are used as-is.
- **No e-file or output of a filable return.**
- ADR-0026's named interest deferrals (K-1, market discount, subtractive
  adjustments) remain deferred; if the owner's real 1099-INT surfaces one of
  them, that is a named blocked disposition, not silent scope growth.

## Contracts

### Existing (build on, do not reopen)

ADR-0011/0014–0017 (fact identity, closure, horizons), ADR-0023 (member
transitions), ADR-0024–0026 (conditions, expressions, interest composition),
ADR-0027/0028 (manifests, package surface — D3 discharges named production
conditions), ADR-0020/0029 (explanations, citations), ADR-0030 (merge units).

### Decided here

D1 residency, D2 contribution, D3 production resolver — each through the
ADR-0005/0013 prototype process with owner-approved `docs/prototypes/<topic>/plan.md`
before first charter, rival evidence per the ADR-0013 amendment, and per-ADR
no-ff merge on ratification.

## Data safety

This milestone is *about* the data boundary, so it is the first milestone
where a mistake can put personal data in the repository. Standing rules for
every track: real values never appear in commits, test fixtures, goldens,
charters, reviews, process logs, or retrospectives; anything derived from real
documents for repo use is re-expressed synthetically; the safety scan runs in
every track's review gate; a track that needs a real-shaped fixture states how
it was synthesized.

## Verification

- The complete in-repo suite (`.venv/bin/python3 -m unittest`), mypy, and
  governance lint stay green and stay fully synthetic.
- A live-run smoke executed by the owner against the out-of-repo workspace is
  the milestone's acceptance evidence. **Corrected 2026-07-16 (D1 finding,
  Ontology §8 governs):** the disposition report *describes* a real run and
  therefore inherits the workspace's sensitivity — it stays in quarantine and
  is **not** cited in in-repo reviews. What crosses into the repo is a
  **non-descriptive attestation** only: that the owner ran the slice, that
  dispositions were observed in quarantine, and that no artifact crossed the
  boundary — never which lines published or blocked or why. (Supersedes the
  prior wording "its *report* (dispositions, not values) is what reviews cite,"
  which conflicted with sensitivity inheritance; the Constitution governance
  note requires such conflicts be corrected by version. ADR-0031 records the
  boundary this rests on.)
- The extended data-safety check is part of the standard gate.

## Exit criteria

1. The owner has contributed real W-2 and 1099-INT facts to a live workspace
   and run the slice: lines 1a/2b/9/11/12/15/16 publish (or block with honest,
   walkable explanations naming what is missing).
2. The repository contains zero personal data, mechanically checked.
3. D1/D2/D3 ratified with rival-backed evidence; ADR-0027/0028 production
   conditions named in the ADRs are discharged or explicitly re-deferred.
4. The W-2 family closes over the owner's declared set.
5. Maturity matrix updated (data-boundary row L0→L3; covered cells L2→L3);
   phase-state briefing rewritten; retrospective written.

## Tracks

Under ADR-0030 each decision topic and each track is its own short-lived
branch with its own review gate and no-ff merge to `main`; there is no
milestone integration branch. Sequencing below is dependency order, not a
single-branch plan.

### Track 0 — Contract decisions (D1, D2, D3)

Three prototype topics, each with an owner-approved plan before its first
charter. D1 and D2 are Tier 3 and interlock (contribution writes into the
residency boundary); their plans may share fixtures but their decisions merge
as separate ADRs. D3 is Tier 2 and may run after D1 ratifies (the resolver
must know where live content lives). Gate-0 decision inventories may conclude
a proposition needs no prototype — that finding is recorded, not assumed.

### Track 1 — Boundary, contribution, and resolver schemas

Schema/contract citizens from the ratified D1, D2, **and D3** ADRs (live
workspace residency, contribution event, provenance linkage, and the production
resolver's publication-root and adoption citizens). Merges after its review gate.

**Amendment (2026-07-17, owner-directed).** Originally scoped to the D1/D2 ADRs;
ADR-0033 (D3) ratified after this Track text was written, and the owner directs
that its **schema citizens** join Track 1 so all three ratified decisions' schema
contracts land together, ahead of the behavior tracks. The D3 additions are
`release-registry.v1` (versioned publication-root citizen; immutable identity
includes the registry document SHA-256) and `act-package-adoption.v1` (the
declared Article-4 user adoption act pinning exact package `{id, version,
checksum}` and release), per ADR-0033 Decision 1 — schemas, positive examples,
named negatives, registry rows, and schema-validation tests, no resolver runtime
behavior. Track 3 retains the resolver *behavior*; only the schema citizens move
here. Consequence: the in-flight Track-1 branch
(`track/frrs-t1-boundary-contribution-schemas`, reviewed 2026-07-17 at D1/D2
scope) must add the two D3 schema citizens before its merge gate; the pre-merge
review's finding F1 is dispositioned by this amendment.

### Track 2 — Contribution machinery

Manual-entry contribution producing member-transition facts with contribution
provenance, over synthetic fixtures in-repo. Includes the negative goldens the
D2 ADR names.

### Track 3 — Production resolver and live workspace bootstrap

D3 implementation *behavior*: resolution beyond the fixture boundary, live
workspace initialization at the D1 location, discharge of the named ADR-0027/0028
production conditions. (D3's *schema citizens* moved to Track 1 per the 2026-07-17
amendment; this track consumes them and implements the resolution behavior over
them.)

### Track 4 — W-2 closure mapping and live-run integration

W-2 closure-mapping content (ADR-0014 pattern); the live-run smoke harness;
the owner's first real run. Acceptance evidence is the disposition report.

### Track 5 — Completion

Maturity-matrix and phase-state updates, retrospective, deferral ledger. No
single milestone merge — completion is a records track, itself reviewed and
merged.

## Principles touched (foreclosure clause)

- **The user controls the context / anti-wizard:** contribution must not become
  a sequencing wizard; it is an event the user initiates with any batch, in any
  order. Any design that forces an entry sequence escalates to Tier 3.
- **Runs consume facts, not inputs:** contribution and execution stay distinct
  product events; a run that reaches around the fact ledger to raw inputs is a
  kill-test failure.
- **Honest blocking:** a real workspace with missing sources must block with a
  walkable explanation — never publish a partial value. Real data makes this
  principle user-visible for the first time.
- **Schema-as-canon / no new noun without a schema:** the contribution event
  and live-workspace citizens get schemas like every other citizen.
- Exceptions to any of the above auto-escalate to Tier 3 per the standing
  protocol.
