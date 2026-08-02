# Charter: Track 3 — Line 16 under D2 (Dividends and Schedule B Slice)

Date: 2026-07-19. Prepared by the foreman. Branch:
`track/dsbs-t3-qdcg-line16`. Governing contracts: **ADR-0038** (the ratified
D2 shape; its five production conditions are this track's scope), ADR-0037
(`conditional_dependency_set` — the substrate, already production-hardened
in Track 0a), ADR-0035 (the `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal the
contradiction interlock consumes; the admission-check mechanism precedent),
ADR-0036 (the taxpayer-assertion categorical `{yes, no}` pattern the
declared-absence citizens instantiate), the milestone plan's Track 3 section
and Contracts/Data-safety/Verification sections
(`docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/dividends-schedule-b-slice.md`), and
the D2 prototype record (`docs/archive/2026-08-02-milestone-artifacts/prototypes/qdcg-worksheet/`, especially
`repair2/design.md` and `reviews/confirmation-r2.md` — the confirmed design
this track productionizes).

## Scope basis

The milestone plan's Track 3 sentence ("the ratified line-16 shape
implemented with honest blocking; goldens for qualified-present and
qualified-absent paths from the authoritative surface") is now concretely
bound by ADR-0038's **Production conditions** section, which names five
items "owed to milestone Track 3; never allowlisted." This charter is those
five conditions, nothing more. Unlike Track 2, no scope judgment call is
needed — the ADR enumerates the track.

## Goal

Make line 16 honest under qualified dividends on the production surface:
the QDCG worksheet as the single declared `rule-artifact.v3` successor rule,
its two capital-gain inputs bound to contributed declared-absence facts
(never assumed), the qualified-zero reduction grounded in
`conditional_dependency_set`'s own false-condition contract, and the
bidirectional admission-locus interlock that keeps a declared "no" honest
against a contributed contradicting signal — all demonstrated through
coordinator-from-facts goldens.

## Deliverables

1. **Declared-absence fact-type citizens (ADR-0038 decision 1, production
   condition 1).** Two taxpayer-assertion fact types on the committed
   ADR-0032/ADR-0036 pattern — categorical `{yes, no}` domain, never
   boolean, no default, presence-before-value:
   `tax.us.2025.capital-gain-distributions` (whether the taxpayer has
   capital-gain distributions to declare) and
   `tax.us.2025.schedule-d-required` (whether Schedule D is required) —
   exact IDs at builder discretion within the committed naming pattern;
   follow the Track 2 `scheduleb.bundle.json` precedent (bundle-adoption,
   not bare members — a bare `fact-type.v2` member passes package
   validation but the live kernel registry rejects assertions referencing
   it). Package admission must **reject a non-`{yes, no}` domain** for
   these citizens, with a test proving the rejection.

2. **The line-16 `rule-artifact.v3` successor rule and package pin
   (ADR-0038 decision 2, production condition 2).** One versioned v3
   successor owns line 16 — no dual producers, no `conflict_semantics` as a
   dynamic selector. Its guard places a `conditional_dependency_set` node
   (condition: qualified dividends > 0; members: the two declaration refs)
   **first and unconditionally in the outer `all`**, so the node's own
   false-condition contract — not incidental operand ordering — grounds the
   qualified-zero reduction (this exact placement is the confirmed Repair 2
   shape; do not reorder). The package pin moves the adopted line-16
   producer from its current version to this v3 successor — the
   `conditional_dependency_set` op is schema-admissible **only under
   `rule-artifact.v3`** (confirmed by direct schema inspection in Repair 2
   and Confirmation R2; a v2 authoring attempt is a hard validation error,
   not a fallback). When both declarations are present: both `"no"`
   publishes the worksheet result; either `"yes"` yields the committed
   `inapplicable`/`guard_inapplicable` disposition — structurally distinct
   from the absence path, no exception, no custom blocked code (a
   `DECLARATION_OUT_OF_SCOPE`-style code was explicitly rejected in
   ADR-0038's alternatives; do not add one).

3. **QDCG ladder parameters and intermediates (ADR-0038 decision 3,
   production condition 3).** The worksheet ladder — preferential-base
   binding, ordinary-portion subtraction, rate-slice comparison, final
   minimum — expressed entirely in the closed committed expression
   vocabulary (`choose`/`compare`/`subtract`/`max`/`bracket_fold`/`round`)
   over versioned parameter declarations. **No new evaluator operation**;
   if the ladder appears to need one, that is a charter-stop finding to
   escalate, not a change to make. Qualified dividends of zero must reach
   the existing ordinary-bracket computation unchanged and read neither
   declaration (verify via the pin/access log, not by inspection).

4. **Bidirectional admission-locus contradiction interlock (ADR-0038
   decision 5, production condition 4).** A current
   capital-gain-distributions declaration of `"no"` and the
   `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal (a contributed 1099-DIV
   box 2a, ADR-0035) may never both be current. Enforcement is
   admission-locus, pre-mutation rejection, reusing the ADR-0035-style
   admission-check mechanism Track 2's subset invariant already extended
   (`registry.subset_invariant_pairs` precedent — a new hook kind is
   acceptable if the pair-shape doesn't fit, a new admitted citizen is not,
   unless implementation demonstrates one necessary; that demonstration is
   an escalation, not a unilateral call). **Kill-tested in all three
   orders**: declaration-first (signal contribution rejects), signal-first
   (declaration contribution rejects), and same-batch (ADR-0032 terminal
   batch semantics — the batch fails closed). A violating pair is never
   recorded.

5. **Structural no-reach-around demonstration (ADR-0038 production
   condition 5).** The worksheet's declared bindings do not and cannot
   include box 2a, its signal, or any recorded-non-composable content —
   demonstrated structurally, following the Track 2
   `AttachmentCannotPropagateToALine` precedent: a committed test asserting
   the line-16 successor's content names none of those symbols/fact-type
   IDs anywhere, so the only path from a real capital-gain distribution to
   line 16 is the deliverable-4 hard error.

## Verification — authoritative-surface golden classes (mandatory, named)

Per the milestone's promoted lesson and the Track 0a/Track 2 discipline —
**every one of the following six named classes must be an executed golden
entering through `live_coordinate_run` from an authoritative act log, never
a `RunContext` shortcut** (confirm by grep at handoff, as Track 2 did:
`RunContext(` may appear only in explicitly docstring-labeled
non-substitutive supplementary classes):

1. **Qualified-positive, both declarations present (`"no"`/`"no"`)** —
   worksheet publishes, result strictly below the ordinary-bracket result
   for the same income, both declarations and the condition pinned.
2. **Qualified-zero reduction** — ordinary-bracket result unchanged,
   neither declaration read, named, or pinned.
3. **Qualified-positive, both declarations absent** — one non-publication
   walk naming **both** missing declarations.
4. **Qualified-positive, exactly one declaration absent** — the walk names
   **that one only** (run for each declaration absent alone; never more
   than the true absent set).
5. **Each present-`"yes"` outcome** — capital-gain-distributions `"yes"`
   and schedule-d-required `"yes"`, each yielding the
   `inapplicable`/`guard_inapplicable` disposition, structurally distinct
   from the absence path.
6. **Declaration supersession displacement** — a published line-16 result
   displaced to non-current when either pinned declaration is superseded
   (the existing two-edge model; a contribution resolving a blocked absence
   is observed by a new run, not a third edge kind).

The deliverable-4 interlock kill-tests (three orders) may be
admission-level tests rather than coordinator goldens where the defect is
not fact-log-observable — but must be executed, not asserted by comment.

**Carried lesson (block-code split, Track 2):** when a composing rule's
`requires` names a symbol that itself blocked, the composing rule reports
`DEPENDENCY_ABSENT` (its `when` never runs) while the blocked rule carries
its own code — check the committed goldens (`unclosed_interest_composition`
and Track 2's) before asserting any block code in a new golden; don't
assume.

**Package versioning:** ship as the next `core-calculations` version at the
next distinct synthetic scope year (v5 used 2054), so every prior version
stays independently exercisable; regenerate derived registry/release
checksums; adoption fixture follows the committed pattern. If the
reachability walker lacks an adjacency case for any new structure, the
sanctioned `entrypoints` listing is the precedented mechanism (Track 2,
`dividend-universe.v1`).

Additionally: full `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m
mypy`, `.venv/bin/python3 tools/governance_lint.py`, and
`.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — all green
before handoff.

## Boundary

No Schedule D content of any kind — `schedule-d-required` is a declaration
citizen only; a `"yes"` yields the inapplicable disposition, never Schedule
D machinery (a future milestone's ground). No 1099-DIV closure-mapping
content or live-run/workspace integration (Track 4). No new evaluator
operations, no new blocked/walk vocabulary codes, no new disposition
shapes. Does not reopen ADR-0035/0036/0037/0038 ratified decisions or
Track 0a/1/2 citizens, except where deliverable 4's admission interlock
requires new code in the admission path — additive only. Owner-held run
tooling (`tools/scaffold_live_acts.py`, `workspace-seed/`) stays untracked.
All fixtures and goldens are manufactured `demo.*`/`demo-*` data per the
milestone's Data-safety section; values, dispositions, refusal reasons, and
workspace location never enter the repo or any review.

## Review gate

One integrated per-track branch and review unit (ADR-0030): an
author-independent pre-merge review follows completion; the owner holds the
merge. Builder dispatch is separately gated on explicit owner release
(ADR-0034); this charter does not authorize dispatch.
