# Charter: Track 3 — Production Resolver and Live Workspace Bootstrap

Date: 2026-07-18. Foreman-authored implementation charter, **proposed for owner
approval** before implementation. Milestone: First Real Return Slice; Track 3 of
the amended Tracks. Lands on `track/frrs-t3-resolver-bootstrap`; branch +
author-independent pre-merge review gate + owner-held no-ff merge (ADR-0030).

- **Type:** implementation track (single implementer + author-independent pre-merge
  review gate; no rival — the D3 prototype structure is already discharged, ADR-0033).
- **Implements:** ADR-0033 (D3) resolution *behavior* over the Track-1 D3 schema
  citizens, plus the D1 installed-residency gates and the ADR-0032 F1 condition
  this track inherits. **Still synthetic — no personal data.** The owner's first
  *real* run is Track 4; Track 3 stands up the machinery and proves it on
  synthetic release/adoption/workspace fixtures and kill/golden coverage.

## Objective

A run resolves its package from **one current, scoped user adoption act** —
never a caller-provided id, path, catalog, or fixture `adoption_pin` — through a
verified release, verified registry bytes, and verified package/member pins into a
strict `validation.ok == True` exclusive member graph, or it refuses. The live
workspace is initialized at the D1 residency location behind the capability wall,
and the raw evaluator path (F1) is closed so "live run" has no structural route to
a hand-assembled input. Every ADR-0033 authority substitution is closed
fail-closed by an executed kill-test.

## Deliverables

1. **Release-rooted, current-user adoption resolver (ADR-0033 Decision 1).** At a
   fixed workspace revision and declared run scope, consider only well-formed
   `act-package-adoption.v1` acts by the sole user in that scope; apply
   supersession; select the unique maximum revision. Zero candidates or a tied
   maximum **refuses**. A non-user act, a stale act, or a runner argument never
   selects authority. Typed refusals, not exceptions-as-control-flow.
2. **Verify release bytes before registry entries authenticate supply (Decision 2).**
   Load the adoption-pinned release from the immutable publication surface, verify
   its exact bytes against the adoption pin, then verify each registry document
   against the release's attested checksum (`release-registry.v1`). Only verified
   registry bytes authenticate the adopted package and members. Close three
   substitutions fail-closed with kill-tests: forged release; replaced registry
   bytes under an honest release; changed package/member bytes under an honest
   verified registry.
3. **Resolve one exclusive, verified member graph or refuse (Decision 3).** Walk
   only exact package-member pins; admit a body only when its canonical checksum
   matches the verified expected digest; byte-identical duplicates collapse; any
   unresolved ambiguity refuses. Filesystem / glob / directory order must not
   affect admission; co-located unpinned files never become candidates and are
   inert. Return no resolved graph, execution, or rendering unless
   `validation.ok == True`; contained issues are reported in the refusal and never
   authorize a clean subset or allowlist.
4. **Live workspace bootstrap at the D1 residency location.** Initialize the live
   out-of-repo workspace `L` behind the ADR-0031 capability wall: the residency
   boundary's installed gates (classification, commit + push envelope) are active
   over live artifacts, not only validated in-test. No committed locator; the
   location is supplied by capability, not repository content. Discharge the D1
   installed-residency/leak production conditions owed to this track (Track-1
   review F2; ADR-0031 production conditions).
5. **Close the raw evaluator as a live path (ADR-0032 F1, inherited).** Make
   `packages.derivation.runner.run` / `runners/derive.py._context` unreachable from
   the production entrypoint — private module, marshalling-token parameter, or
   import fence — so the runs-consume-facts guarantee covers the evaluator and not
   only `live_run`'s signature. An executed test proves no production path reaches
   a hand-assembled `InputFinding`.
6. **Named ADR-0027/0028 production conditions (D3 ledger).** Discharge the
   `CS`-and-owning-track conditions the ADR-0033 §4 ledger assigns to Track 3
   (PC1 unpinned-co-located golden; PC2 conflict-semantics golden; PC3
   registry-verified package and members), and explicitly carry the `PC(T4)`
   items to Track 4 in the closing note.
7. **Synthetic kill/golden corpus.** Executed (not asserted) coverage for release
   substitution, adoption currency (stale / tied / non-user), same-key handling,
   missing pins, package/member mismatch, filesystem-order independence, and
   hard-gate refusal-with-contained-issues.

## RG-1 — decision point for the owner (see Scope boundary below)

ADR-0033 Decision 5 names **RG-1** — repair of the committed core package's eight
contained issues (four `MEMBER_UNREACHABLE`, plus `SCHEMA_NOT_ADMITTED`,
`ROLE_MISMATCH`, two `MAPPING_FACT_TYPE_NOT_ADMITTED`) — as a **MUST** prerequisite
before a live package family crosses the hard gate, with no leniency or allowlist.
RG-1 is *content* repair, not resolver machinery. This charter's **default**
places RG-1 in **Track 4** (adjacent to the first real run it gates), leaving
Track 3 to prove the resolver and gate refuse the un-repaired package. The owner
may instead pull RG-1 into Track 3. This is the single scope decision this charter
surfaces.

## Scope fence (do not cross)

- **No real personal data.** Synthetic release/adoption/workspace fixtures only;
  the live workspace is bootstrapped and exercised with synthetic artifacts. The
  owner's first real run is **Track 4**.
- **No W-2 closure mapping, no live-run smoke harness, no first real run** — Track 4.
  **No OCR, no UI.**
- **RG-1 core-package content repair defaults to Track 4** (see decision point);
  do not repair core-package content here unless the owner moves RG-1 into Track 3.
- Do not edit the ratified ADRs or the Track-1 schema citizens (implement to them;
  a genuine schema defect is surfaced, not patched).

## Verification (all green, re-run and reported)

- Full suite green, fully synthetic; `mypy packages tools tests` clean;
  `governance_lint.py` conformant.
- Every ADR-0033 substitution and the F1 evaluator-closure are **executed**
  kill-tests, not asserted stubs.
- The hard gate returns no graph/execution/rendering on `validation.ok == False`,
  proven by golden.
- Data-safety scan clean; every identifier/value synthetic (`demo.*`).

## Review gate

Author-independent pre-merge review before merge (a charter for it is authored when
the branch is ready), findings classified blocking / scope defect / production
condition / non-blocking. Owner-held merge (ADR-0030); owner-approved dispatch of
any sub-agent (ADR-0034).

## Exit criteria

A synthetic current-user adoption resolves through verified release → verified
registry → verified package/member pins into a `validation.ok == True` exclusive
graph, or refuses with typed reasons; every ADR-0033 substitution is closed by an
executed kill-test; the live workspace initializes behind the D1 capability wall
with installed residency gates active; the raw evaluator path is structurally
closed (F1); the named T3 ADR-0027/0028 conditions are discharged and the T4 ones
carried; all verification green. RG-1 and the first real run are carried to Track 4
(or RG-1 pulled in per the owner's scope decision).
